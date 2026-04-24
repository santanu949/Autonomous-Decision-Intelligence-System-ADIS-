"""
ADIS Forecasting Engine - Linear regression-based forecasting.
Pure Python implementation (no sklearn dependency required).
"""
import math
from typing import List, Dict, Any
from core.models import MLModelResult, ForecastPoint


class ForecastingEngine:
    """Simple linear regression forecasting for each numeric variable."""

    def forecast(self, data: List[Dict[str, Any]],
                 numeric_keys: List[str],
                 forecast_periods: int = 3) -> List[MLModelResult]:
        """Generate forecasts for each numeric variable using linear regression."""
        results = []

        for key in numeric_keys:
            values = [float(row.get(key, 0)) for row in data]
            if len(values) < 3:
                continue

            # Fit linear regression: y = mx + b
            n = len(values)
            x = list(range(n))
            slope, intercept, r_squared = self._linear_regression(x, values)

            if r_squared is None:
                continue

            # Generate forecasts
            forecasts = []
            residuals = [values[i] - (slope * i + intercept) for i in range(n)]
            std_residual = math.sqrt(sum(r ** 2 for r in residuals) / max(1, n - 2)) if n > 2 else 0

            for p in range(1, forecast_periods + 1):
                x_pred = n + p - 1
                predicted = slope * x_pred + intercept
                # Prediction interval widens with distance
                margin = 1.96 * std_residual * math.sqrt(1 + 1/n + (x_pred - sum(x)/n)**2 / sum((xi - sum(x)/n)**2 for xi in x)) if std_residual > 0 else 0

                forecasts.append(ForecastPoint(
                    period=f"Period {n + p}",
                    predicted_value=round(predicted, 2),
                    lower_bound=round(predicted - margin, 2),
                    upper_bound=round(predicted + margin, 2),
                    confidence=round(max(30, min(95, r_squared * 100 - p * 5)), 1)
                ))

            # Feature importance (simple: index as only feature)
            feature_importance = {"trend_coefficient": round(abs(slope) / (abs(intercept) + 1), 4) if intercept != 0 else 1.0}

            results.append(MLModelResult(
                model_type="regression",
                target_variable=key,
                accuracy_metric="r_squared",
                accuracy_value=round(r_squared, 4),
                feature_importance=feature_importance,
                forecasts=forecasts
            ))

        return results

    def _linear_regression(self, x: List[float], y: List[float]):
        """Simple least-squares linear regression."""
        n = len(x)
        if n < 2:
            return 0, 0, None

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(xi ** 2 for xi in x)

        denom = n * sum_x2 - sum_x ** 2
        if denom == 0:
            return 0, sum_y / n, None

        slope = (n * sum_xy - sum_x * sum_y) / denom
        intercept = (sum_y - slope * sum_x) / n

        # R² calculation
        mean_y = sum_y / n
        ss_tot = sum((yi - mean_y) ** 2 for yi in y)
        ss_res = sum((y[i] - (slope * x[i] + intercept)) ** 2 for i in range(n))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        return slope, intercept, max(0, r_squared)
