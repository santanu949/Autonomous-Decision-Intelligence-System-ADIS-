"""
ADIS Adaptive Parser - Intelligently infer structure from ambiguous inputs.
Handles JSON, CSV-like structures, and mixed data with robust error handling.
"""
import math
import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime
from core.models import DataProfile, VariableProfile, VariableType

logger = logging.getLogger(__name__)


class AdaptiveParser:
    """
    Validates, normalizes, and classifies incoming data.
    Produces a DataProfile and clean data for downstream processing.
    """

    TEMPORAL_PATTERNS = [
        "date", "time", "timestamp", "created", "updated", "year", "month",
        "day", "period", "quarter", "week"
    ]

    def parse(self, raw_data: Any) -> Dict[str, Any]:
        """
        Main entry point: parse raw data into validated, normalized format.
        Returns dict with 'data', 'profile', 'numeric_keys', 'categorical_keys', 'temporal_keys'.
        """
        # Validate input structure
        if not raw_data:
            raise ValueError("Empty data provided. Expected a list of JSON objects.")
        if not isinstance(raw_data, list):
            raise ValueError(f"Expected list of objects, got {type(raw_data).__name__}")
        if not all(isinstance(row, dict) for row in raw_data):
            raise ValueError("Each data item must be a JSON object (dict).")

        # Classify variables
        numeric_keys, categorical_keys, temporal_keys = self._classify_variables(raw_data)

        # Normalize data
        validated_data = self._normalize(raw_data, numeric_keys, categorical_keys, temporal_keys)

        # Build profile
        profile = self._build_profile(validated_data, numeric_keys, categorical_keys, temporal_keys)

        return {
            "data": validated_data,
            "profile": profile,
            "numeric_keys": numeric_keys,
            "categorical_keys": categorical_keys,
            "temporal_keys": temporal_keys
        }

    def _classify_variables(self, data: List[Dict[str, Any]]) -> Tuple[List[str], List[str], List[str]]:
        """Classify each column by type using heuristics across all rows."""
        if not data:
            return [], [], []

        # Collect all keys across all rows
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())

        numeric_keys = []
        categorical_keys = []
        temporal_keys = []

        for key in all_keys:
            values = [row.get(key) for row in data if key in row and row[key] is not None]
            if not values:
                categorical_keys.append(key)
                continue

            # Check temporal by name
            if any(pat in key.lower() for pat in self.TEMPORAL_PATTERNS):
                temporal_keys.append(key)
                continue

            # Check numeric
            numeric_count = sum(1 for v in values if isinstance(v, (int, float)))
            str_numeric_count = 0
            for v in values:
                if isinstance(v, str):
                    try:
                        float(v.replace(",", "").replace("$", "").replace("%", ""))
                        str_numeric_count += 1
                    except (ValueError, AttributeError):
                        pass

            total_numeric = numeric_count + str_numeric_count
            if total_numeric / len(values) > 0.7:
                numeric_keys.append(key)
            else:
                # Check if it's a boolean column
                bool_vals = {str(v).lower() for v in values}
                if bool_vals.issubset({"true", "false", "1", "0", "yes", "no"}):
                    categorical_keys.append(key)
                else:
                    categorical_keys.append(key)

        return sorted(numeric_keys), sorted(categorical_keys), sorted(temporal_keys)

    def _normalize(self, data: List[Dict[str, Any]],
                   numeric_keys: List[str],
                   categorical_keys: List[str],
                   temporal_keys: List[str]) -> List[Dict[str, Any]]:
        """Normalize all values to consistent types. Handle missing data."""
        normalized = []
        for row in data:
            clean_row = {}

            for k in numeric_keys:
                val = row.get(k)
                if val is None:
                    clean_row[k] = 0.0
                elif isinstance(val, (int, float)):
                    clean_row[k] = float(val)
                elif isinstance(val, str):
                    try:
                        clean_row[k] = float(val.replace(",", "").replace("$", "").replace("%", ""))
                    except ValueError:
                        clean_row[k] = 0.0
                else:
                    clean_row[k] = 0.0

            for k in categorical_keys:
                clean_row[k] = str(row.get(k, "Unknown"))

            for k in temporal_keys:
                clean_row[k] = str(row.get(k, ""))

            normalized.append(clean_row)

        return normalized

    def _build_profile(self, data: List[Dict[str, Any]],
                       numeric_keys: List[str],
                       categorical_keys: List[str],
                       temporal_keys: List[str]) -> DataProfile:
        """Build a comprehensive data quality profile."""
        all_keys = set(numeric_keys + categorical_keys + temporal_keys)
        variables = []

        for key in sorted(all_keys):
            values = [row.get(key) for row in data]
            non_null = [v for v in values if v is not None and v != "" and v != "Unknown"]

            if key in numeric_keys:
                vtype = VariableType.NUMERIC
            elif key in temporal_keys:
                vtype = VariableType.TEMPORAL
            else:
                vtype = VariableType.CATEGORICAL

            vp = VariableProfile(
                name=key,
                var_type=vtype,
                count=len(values),
                missing=len(values) - len(non_null),
                unique=len(set(str(v) for v in non_null))
            )

            if key in numeric_keys:
                num_vals = [float(v) for v in non_null if isinstance(v, (int, float))]
                if num_vals:
                    vp.mean = sum(num_vals) / len(num_vals)
                    sorted_vals = sorted(num_vals)
                    n = len(sorted_vals)
                    vp.median = sorted_vals[n // 2] if n % 2 else (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
                    vp.min_val = min(num_vals)
                    vp.max_val = max(num_vals)
                    variance = sum((x - vp.mean) ** 2 for x in num_vals) / len(num_vals)
                    vp.std_dev = math.sqrt(variance) if variance > 0 else 0.0
                    # Quartiles
                    vp.q1 = sorted_vals[n // 4] if n >= 4 else vp.min_val
                    vp.q3 = sorted_vals[3 * n // 4] if n >= 4 else vp.max_val
                    vp.iqr = vp.q3 - vp.q1

            elif key in categorical_keys:
                from collections import Counter
                counts = Counter(str(v) for v in non_null)
                vp.top_values = dict(counts.most_common(10))

            variables.append(vp)

        # Quality metrics
        total_cells = len(data) * len(all_keys) if all_keys else 1
        missing_cells = sum(vp.missing for vp in variables)
        completeness = ((total_cells - missing_cells) / total_cells * 100) if total_cells > 0 else 0

        issues = []
        for vp in variables:
            if vp.missing > 0:
                issues.append(f"'{vp.name}' has {vp.missing} missing values")
            if vp.var_type == VariableType.NUMERIC and vp.unique == 1:
                issues.append(f"'{vp.name}' is constant (no variance)")

        quality_score = min(100, completeness - len(issues) * 5)

        return DataProfile(
            row_count=len(data),
            column_count=len(all_keys),
            variables=variables,
            quality_score=max(0, quality_score),
            completeness=completeness,
            issues=issues
        )
