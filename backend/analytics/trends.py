"""
ADIS Trend Analyzer - Detect trends, patterns, and generate trend insights.
"""
from typing import List, Dict, Any
from core.models import Insight, VariableProfile


class TrendAnalyzer:
    """Analyzes trends in time-series and sequential data."""

    def analyze(self, data: List[Dict[str, Any]],
                numeric_keys: List[str],
                profiles: Dict[str, VariableProfile],
                categorical_keys: List[str]) -> List[Insight]:
        """Generate trend-based insights from variable profiles."""
        insights = []

        for key in numeric_keys:
            if key not in profiles:
                continue
            profile = profiles[key]
            values = [row.get(key, 0.0) for row in data]

            if not values or len(values) < 2:
                continue

            # Trend direction insight
            if profile.trend_direction == "increasing":
                pct = profile.trend_pct_change or 0
                insights.append(Insight(
                    category="trend",
                    title=f"Upward trend in {key}",
                    description=f"{key} shows a positive growth trend with {pct:+.1f}% change from first to last value "
                                f"(from {values[0]:,.2f} to {values[-1]:,.2f}).",
                    severity="info",
                    confidence=min(95, 50 + abs(pct) * 0.5),
                    contributing_factors=[key],
                    data_evidence={"start": values[0], "end": values[-1], "change_pct": pct}
                ))
            elif profile.trend_direction == "decreasing":
                pct = profile.trend_pct_change or 0
                severity = "warning" if abs(pct) > 20 else "info"
                insights.append(Insight(
                    category="trend",
                    title=f"Declining trend in {key}",
                    description=f"{key} shows a declining trend with {pct:+.1f}% change "
                                f"(from {values[0]:,.2f} to {values[-1]:,.2f}).",
                    severity=severity,
                    confidence=min(95, 50 + abs(pct) * 0.5),
                    contributing_factors=[key],
                    data_evidence={"start": values[0], "end": values[-1], "change_pct": pct}
                ))

            # Volatility insight
            if profile.std_dev and profile.mean and profile.mean != 0:
                cv = (profile.std_dev / abs(profile.mean)) * 100
                if cv > 50:
                    insights.append(Insight(
                        category="pattern",
                        title=f"High volatility in {key}",
                        description=f"{key} exhibits high volatility with a coefficient of variation of {cv:.1f}%. "
                                    f"Values range from {profile.min_val:,.2f} to {profile.max_val:,.2f}.",
                        severity="warning",
                        confidence=min(90, cv * 0.5),
                        contributing_factors=[key],
                        data_evidence={"cv": cv, "std_dev": profile.std_dev, "mean": profile.mean}
                    ))

            # Distribution skewness
            if profile.skewness and abs(profile.skewness) > 1:
                direction = "right" if profile.skewness > 0 else "left"
                insights.append(Insight(
                    category="distribution",
                    title=f"Skewed distribution in {key}",
                    description=f"{key} has a {direction}-skewed distribution (skewness: {profile.skewness:.2f}), "
                                f"indicating {('more high outliers' if direction == 'right' else 'more low outliers')}.",
                    severity="info",
                    confidence=min(85, abs(profile.skewness) * 30),
                    contributing_factors=[key]
                ))

            # Concentration analysis (gap between mean and median)
            if profile.mean and profile.median:
                gap_pct = abs(profile.mean - profile.median) / abs(profile.mean) * 100 if profile.mean != 0 else 0
                if gap_pct > 15:
                    insights.append(Insight(
                        category="distribution",
                        title=f"Mean-median divergence in {key}",
                        description=f"The mean ({profile.mean:,.2f}) and median ({profile.median:,.2f}) of {key} "
                                    f"differ by {gap_pct:.1f}%, suggesting influential outliers.",
                        severity="info",
                        confidence=min(80, gap_pct * 2),
                        contributing_factors=[key]
                    ))

            # Consecutive movement analysis
            movements = self._analyze_movements(values)
            if movements["longest_streak"] >= 3:
                insights.append(Insight(
                    category="pattern",
                    title=f"Sustained {movements['streak_direction']} streak in {key}",
                    description=f"{key} showed {movements['longest_streak']} consecutive periods of "
                                f"{movements['streak_direction']} movement, suggesting a sustained pattern.",
                    severity="info",
                    confidence=min(80, movements['longest_streak'] * 15),
                    contributing_factors=[key]
                ))

        # Cross-variable insights
        if len(numeric_keys) >= 2:
            insights.extend(self._cross_variable_insights(data, numeric_keys, profiles))

        return insights

    def _analyze_movements(self, values: List[float]) -> Dict[str, Any]:
        """Analyze consecutive movement patterns."""
        if len(values) < 2:
            return {"longest_streak": 0, "streak_direction": "stable"}

        current_streak = 1
        longest_streak = 1
        streak_dir = "stable"

        for i in range(1, len(values)):
            diff = values[i] - values[i - 1]
            if i == 1:
                current_dir = "increasing" if diff > 0 else ("decreasing" if diff < 0 else "stable")
            else:
                prev_diff = values[i - 1] - values[i - 2]
                prev_dir = "increasing" if prev_diff > 0 else ("decreasing" if prev_diff < 0 else "stable")
                current_dir = "increasing" if diff > 0 else ("decreasing" if diff < 0 else "stable")

                if current_dir == prev_dir and current_dir != "stable":
                    current_streak += 1
                else:
                    current_streak = 1

            if current_streak > longest_streak:
                longest_streak = current_streak
                streak_dir = current_dir

        return {"longest_streak": longest_streak, "streak_direction": streak_dir}

    def _cross_variable_insights(self, data: List[Dict[str, Any]],
                                  numeric_keys: List[str],
                                  profiles: Dict[str, VariableProfile]) -> List[Insight]:
        """Generate insights from relationships between variables."""
        insights = []

        # Ratio analysis for common business pairs
        ratio_pairs = [
            ("sales", "expenses", "profit margin"),
            ("revenue", "cost", "efficiency ratio"),
            ("income", "expenses", "net margin"),
        ]

        for key_a, key_b, label in ratio_pairs:
            if key_a in profiles and key_b in profiles:
                a_mean = profiles[key_a].mean or 0
                b_mean = profiles[key_b].mean or 0
                if a_mean > 0:
                    ratio = (a_mean - b_mean) / a_mean * 100
                    insights.append(Insight(
                        category="ratio",
                        title=f"{label.title()}: {ratio:.1f}%",
                        description=f"Average {key_a} ({a_mean:,.2f}) vs average {key_b} ({b_mean:,.2f}) "
                                    f"yields a {label} of {ratio:.1f}%.",
                        severity="critical" if ratio < 0 else ("warning" if ratio < 10 else "info"),
                        confidence=85,
                        contributing_factors=[key_a, key_b],
                        data_evidence={"ratio": ratio, "mean_a": a_mean, "mean_b": b_mean}
                    ))

        return insights
