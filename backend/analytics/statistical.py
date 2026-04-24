"""
ADIS Statistical Engine - Full statistical profiling for each numeric variable.
Computes: mean, median, std_dev, quartiles, IQR, skewness, kurtosis.
"""
import math
from typing import List, Dict, Any
from core.models import VariableProfile, VariableType


class StatisticalEngine:
    """Performs comprehensive statistical analysis on validated data."""

    def analyze(self, data: List[Dict[str, Any]],
                numeric_keys: List[str],
                categorical_keys: List[str]) -> Dict[str, VariableProfile]:
        """Analyze all variables and return profiles keyed by variable name."""
        profiles = {}

        for key in numeric_keys:
            values = [row.get(key, 0.0) for row in data]
            values = [float(v) for v in values if v is not None]

            if not values:
                continue

            n = len(values)
            sorted_vals = sorted(values)

            # Central tendency
            mean = sum(values) / n
            median = self._median(sorted_vals)

            # Dispersion
            variance = sum((x - mean) ** 2 for x in values) / n
            std_dev = math.sqrt(variance) if variance > 0 else 0.0

            # Quartiles
            q1 = self._percentile(sorted_vals, 25)
            q3 = self._percentile(sorted_vals, 75)
            iqr = q3 - q1

            # Shape
            skewness = self._skewness(values, mean, std_dev) if std_dev > 0 else 0.0
            kurtosis = self._kurtosis(values, mean, std_dev) if std_dev > 0 else 0.0

            # Trend (sequential)
            trend_mag = values[-1] - values[0] if n > 1 else 0.0
            trend_pct = (trend_mag / abs(values[0]) * 100) if values[0] != 0 else 0.0
            if trend_mag > 0:
                trend_dir = "increasing"
            elif trend_mag < 0:
                trend_dir = "decreasing"
            else:
                trend_dir = "stable"

            profiles[key] = VariableProfile(
                name=key,
                var_type=VariableType.NUMERIC,
                count=n,
                missing=0,
                unique=len(set(values)),
                mean=round(mean, 4),
                median=round(median, 4),
                std_dev=round(std_dev, 4),
                min_val=min(values),
                max_val=max(values),
                q1=round(q1, 4),
                q3=round(q3, 4),
                iqr=round(iqr, 4),
                skewness=round(skewness, 4),
                kurtosis=round(kurtosis, 4),
                trend_direction=trend_dir,
                trend_magnitude=round(trend_mag, 4),
                trend_pct_change=round(trend_pct, 2)
            )

        for key in categorical_keys:
            values = [row.get(key, "Unknown") for row in data]
            from collections import Counter
            counts = Counter(str(v) for v in values)

            profiles[key] = VariableProfile(
                name=key,
                var_type=VariableType.CATEGORICAL,
                count=len(values),
                missing=sum(1 for v in values if v is None or str(v) == "Unknown"),
                unique=len(counts),
                top_values=dict(counts.most_common(10))
            )

        return profiles

    def _median(self, sorted_vals: List[float]) -> float:
        n = len(sorted_vals)
        if n == 0:
            return 0.0
        if n % 2 == 1:
            return sorted_vals[n // 2]
        return (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2

    def _percentile(self, sorted_vals: List[float], pct: float) -> float:
        n = len(sorted_vals)
        if n == 0:
            return 0.0
        if n == 1:
            return sorted_vals[0]
        k = (pct / 100) * (n - 1)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_vals[int(k)]
        return sorted_vals[f] * (c - k) + sorted_vals[c] * (k - f)

    def _skewness(self, values: List[float], mean: float, std: float) -> float:
        n = len(values)
        if n < 3 or std == 0:
            return 0.0
        return (n / ((n - 1) * (n - 2))) * sum(((x - mean) / std) ** 3 for x in values)

    def _kurtosis(self, values: List[float], mean: float, std: float) -> float:
        n = len(values)
        if n < 4 or std == 0:
            return 0.0
        kurt = (n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3)) * sum(((x - mean) / std) ** 4 for x in values)
        kurt -= (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))
        return kurt
