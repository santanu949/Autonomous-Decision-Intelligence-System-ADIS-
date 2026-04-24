"""
ADIS Correlation Analyzer - Compute pairwise Pearson correlations 
and classify relationship strength.
"""
import math
from typing import List, Dict, Any
from core.models import CorrelationPair


class CorrelationAnalyzer:
    """Analyzes correlations between all numeric variable pairs."""

    def analyze(self, data: List[Dict[str, Any]],
                numeric_keys: List[str]) -> List[CorrelationPair]:
        """Compute pairwise correlations for all numeric variables."""
        correlations = []

        if len(numeric_keys) < 2 or len(data) < 3:
            return correlations

        for i, var_a in enumerate(numeric_keys):
            for var_b in numeric_keys[i + 1:]:
                vals_a = [float(row.get(var_a, 0)) for row in data]
                vals_b = [float(row.get(var_b, 0)) for row in data]

                r = self._pearson(vals_a, vals_b)
                if r is None:
                    continue

                strength = self._classify_strength(abs(r))
                direction = "positive" if r > 0 else "negative"

                # Significance test (t-test for correlation)
                n = len(vals_a)
                significant = self._is_significant(r, n)

                correlations.append(CorrelationPair(
                    var_a=var_a,
                    var_b=var_b,
                    coefficient=round(r, 4),
                    strength=strength,
                    direction=direction,
                    significance="significant" if significant else "not_significant"
                ))

        return sorted(correlations, key=lambda c: abs(c.coefficient), reverse=True)

    def _pearson(self, x: List[float], y: List[float]) -> float:
        """Compute Pearson correlation coefficient."""
        n = len(x)
        if n < 2:
            return None

        mean_x = sum(x) / n
        mean_y = sum(y) / n

        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))

        if std_x == 0 or std_y == 0:
            return None

        return cov / (std_x * std_y)

    def _classify_strength(self, abs_r: float) -> str:
        if abs_r >= 0.7:
            return "strong"
        elif abs_r >= 0.4:
            return "moderate"
        elif abs_r >= 0.2:
            return "weak"
        return "negligible"

    def _is_significant(self, r: float, n: int, alpha: float = 0.05) -> bool:
        """Approximate significance using t-test for correlation."""
        if n < 4 or abs(r) >= 1.0:
            return abs(r) > 0.5
        t_stat = r * math.sqrt((n - 2) / (1 - r ** 2))
        # Approximate critical value for two-tailed test
        critical = 2.0 + 2.0 / (n - 2)  # Rough approximation
        return abs(t_stat) > critical
