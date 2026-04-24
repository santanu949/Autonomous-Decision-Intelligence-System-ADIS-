"""
ADIS Decision Synthesizer - Multi-signal aggregation with conflict resolution.
Produces ranked recommendations with supporting evidence.
"""
from typing import List, Dict, Any, Optional
from core.models import (
    Decision, Insight, AnomalyRecord, CorrelationPair,
    VariableProfile, MLModelResult, ConfidenceLevel, RiskLevel,
    FactorContribution
)


class DecisionSynthesizer:
    """
    Aggregates insights, anomalies, correlations, and ML results
    into prioritized, explainable decisions.
    """

    def synthesize(self, data: List[Dict[str, Any]],
                   profiles: Dict[str, VariableProfile],
                   insights: List[Insight],
                   anomalies: List[AnomalyRecord],
                   correlations: List[CorrelationPair],
                   ml_results: List[MLModelResult],
                   numeric_keys: List[str],
                   categorical_keys: List[str]) -> List[Decision]:
        """Generate top-N ranked decisions from all analytical signals."""
        decisions = []

        # Signal 1: Business-specific heuristics (domain patterns)
        decisions.extend(self._business_heuristics(data, profiles, numeric_keys))

        # Signal 2: Anomaly-driven decisions
        decisions.extend(self._anomaly_decisions(anomalies, profiles))

        # Signal 3: Trend-driven decisions
        decisions.extend(self._trend_decisions(profiles, numeric_keys))

        # Signal 4: Correlation-driven decisions
        decisions.extend(self._correlation_decisions(correlations, profiles))

        # Signal 5: ML-driven decisions
        decisions.extend(self._ml_decisions(ml_results, profiles))

        # Fallback: generic if nothing specific
        if not decisions:
            decisions.append(self._generic_decision(profiles, numeric_keys))

        # Rank and deduplicate
        decisions = self._rank_and_deduplicate(decisions)

        # Cap at top 5
        return decisions[:5]

    def _business_heuristics(self, data: List[Dict[str, Any]],
                              profiles: Dict[str, VariableProfile],
                              numeric_keys: List[str]) -> List[Decision]:
        """Domain-specific business logic."""
        decisions = []

        # Revenue/Sales vs Expenses/Cost pattern
        revenue_keys = [k for k in numeric_keys if any(w in k.lower() for w in ["sales", "revenue", "income"])]
        expense_keys = [k for k in numeric_keys if any(w in k.lower() for w in ["expenses", "cost", "spend", "expenditure"])]

        for rev_key in revenue_keys:
            for exp_key in expense_keys:
                if rev_key in profiles and exp_key in profiles:
                    rev_mean = profiles[rev_key].mean or 0
                    exp_mean = profiles[exp_key].mean or 0
                    rev_trend = profiles[rev_key].trend_pct_change or 0
                    exp_trend = profiles[exp_key].trend_pct_change or 0

                    margin = (rev_mean - exp_mean) / rev_mean * 100 if rev_mean > 0 else 0

                    factors = [
                        FactorContribution(
                            factor=f"Average {rev_key}",
                            contribution_pct=40,
                            direction="positive" if rev_mean > exp_mean else "negative",
                            value=rev_mean,
                            description=f"Average {rev_key} is {rev_mean:,.2f}"
                        ),
                        FactorContribution(
                            factor=f"Average {exp_key}",
                            contribution_pct=35,
                            direction="negative" if exp_mean > rev_mean * 0.7 else "positive",
                            value=exp_mean,
                            description=f"Average {exp_key} is {exp_mean:,.2f}"
                        ),
                        FactorContribution(
                            factor=f"{rev_key} trend",
                            contribution_pct=15,
                            direction="positive" if rev_trend > 0 else "negative",
                            value=rev_trend,
                            description=f"{rev_key} trending {rev_trend:+.1f}%"
                        ),
                        FactorContribution(
                            factor=f"{exp_key} trend",
                            contribution_pct=10,
                            direction="positive" if exp_trend < 0 else "negative",
                            value=exp_trend,
                            description=f"{exp_key} trending {exp_trend:+.1f}%"
                        ),
                    ]

                    if margin > 25:
                        decisions.append(Decision(
                            action="Accelerate Growth Investments",
                            category="growth",
                            confidence=min(92, 70 + margin * 0.5),
                            confidence_level=ConfidenceLevel.HIGH,
                            risk_level=RiskLevel.LOW,
                            expected_impact=f"Reinvesting surplus at {margin:.0f}% margin could accelerate growth by 15-25%",
                            explanation=f"Strong margins of {margin:.1f}% indicate room for aggressive growth. {rev_key} averages {rev_mean:,.0f} vs {exp_key} at {exp_mean:,.0f}.",
                            reasoning_chain=[
                                f"Analyzed {rev_key} vs {exp_key} across {len(data)} periods",
                                f"Calculated margin: {margin:.1f}%",
                                f"Margin exceeds 25% threshold → growth investment recommended",
                                f"{rev_key} trend: {rev_trend:+.1f}%, {exp_key} trend: {exp_trend:+.1f}%"
                            ],
                            contributing_factors=factors,
                            alternatives=["Increase dividend payout", "Build cash reserves", "Pursue strategic acquisitions"],
                            supporting_insights=[]
                        ))
                    elif margin > 5:
                        decisions.append(Decision(
                            action="Optimize Operational Efficiency",
                            category="operational",
                            confidence=min(85, 60 + margin * 0.8),
                            confidence_level=ConfidenceLevel.MEDIUM,
                            risk_level=RiskLevel.MODERATE,
                            expected_impact=f"Improving efficiency at {margin:.0f}% margin could save 8-15% on costs",
                            explanation=f"Margins at {margin:.1f}% are positive but narrow. Focus on cost optimization to widen the gap.",
                            reasoning_chain=[
                                f"Margin of {margin:.1f}% is positive but below 25% threshold",
                                f"Efficiency improvements could widen margins by 5-10%",
                                f"Current {exp_key} trajectory: {exp_trend:+.1f}%"
                            ],
                            contributing_factors=factors,
                            alternatives=["Renegotiate vendor contracts", "Automate manual processes", "Review staffing levels"],
                            supporting_insights=[]
                        ))
                    else:
                        decisions.append(Decision(
                            action="Immediate Cost Reduction Required",
                            category="cost",
                            confidence=min(95, 80 + abs(margin) * 0.3),
                            confidence_level=ConfidenceLevel.CRITICAL,
                            risk_level=RiskLevel.SEVERE,
                            expected_impact=f"Without intervention at {margin:.0f}% margin, losses will compound",
                            explanation=f"Critical: margins at {margin:.1f}%. {exp_key} ({exp_mean:,.0f}) is consuming nearly all of {rev_key} ({rev_mean:,.0f}). Urgent cost restructuring needed.",
                            reasoning_chain=[
                                f"Margin of {margin:.1f}% is dangerously low or negative",
                                f"{exp_key} at {exp_mean:,.0f} is {exp_mean/rev_mean*100:.0f}% of {rev_key}" if rev_mean > 0 else f"{exp_key} exceeds {rev_key}",
                                "Immediate expense audit recommended",
                                "Priority: variable costs reduction"
                            ],
                            contributing_factors=factors,
                            alternatives=["Restructure operations", "Divest non-core assets", "Emergency fundraising"],
                            supporting_insights=[]
                        ))

        return decisions

    def _anomaly_decisions(self, anomalies: List[AnomalyRecord],
                            profiles: Dict[str, VariableProfile]) -> List[Decision]:
        """Generate decisions from detected anomalies."""
        if not anomalies:
            return []

        decisions = []
        severe = [a for a in anomalies if a.severity in [RiskLevel.SEVERE, RiskLevel.HIGH]]

        if severe:
            top_anomaly = severe[0]
            factors = [
                FactorContribution(
                    factor=f"Anomaly in {top_anomaly.variable}",
                    contribution_pct=60,
                    direction="negative",
                    value=top_anomaly.value,
                    description=f"Value {top_anomaly.value} deviates {top_anomaly.deviation_score:.1f}σ from expected"
                ),
                FactorContribution(
                    factor="Number of anomalies",
                    contribution_pct=25,
                    direction="negative",
                    value=len(anomalies),
                    description=f"{len(anomalies)} total anomalies detected across all variables"
                ),
                FactorContribution(
                    factor="Detection confidence",
                    contribution_pct=15,
                    direction="neutral",
                    value=top_anomaly.deviation_score,
                    description=f"Detected via {top_anomaly.method} method"
                ),
            ]

            decisions.append(Decision(
                action=f"Investigate {top_anomaly.variable} Anomaly",
                category="risk",
                confidence=min(90, top_anomaly.deviation_score * 20),
                confidence_level=ConfidenceLevel.HIGH,
                risk_level=RiskLevel.HIGH,
                expected_impact=f"Unaddressed anomaly in {top_anomaly.variable} could indicate data quality issues or emerging risks",
                explanation=f"{len(severe)} high-severity anomalies detected. The most critical is in '{top_anomaly.variable}' "
                           f"where value {top_anomaly.value} deviates {top_anomaly.deviation_score:.1f} standard deviations from expected range ({top_anomaly.expected_range}).",
                reasoning_chain=[
                    f"Detected {len(anomalies)} anomalies using multi-method analysis",
                    f"{len(severe)} classified as high/severe severity",
                    f"Top anomaly: {top_anomaly.variable} = {top_anomaly.value} (method: {top_anomaly.method})",
                    f"Expected range: {top_anomaly.expected_range}",
                    "Recommend immediate investigation to determine root cause"
                ],
                contributing_factors=factors,
                alternatives=["Flag for manual review", "Exclude outlier from analysis", "Monitor for recurrence"],
                supporting_insights=[]
            ))

        return decisions

    def _trend_decisions(self, profiles: Dict[str, VariableProfile],
                          numeric_keys: List[str]) -> List[Decision]:
        """Generate decisions from trend analysis."""
        decisions = []

        declining = []
        growing = []

        for key in numeric_keys:
            if key not in profiles:
                continue
            p = profiles[key]
            if p.trend_pct_change is not None:
                if p.trend_pct_change < -15:
                    declining.append((key, p))
                elif p.trend_pct_change > 15:
                    growing.append((key, p))

        if declining:
            worst = max(declining, key=lambda x: abs(x[1].trend_pct_change))
            key, p = worst
            decisions.append(Decision(
                action=f"Address Declining {key.title()}",
                category="strategic",
                confidence=min(85, 50 + abs(p.trend_pct_change) * 0.5),
                confidence_level=ConfidenceLevel.HIGH if abs(p.trend_pct_change) > 30 else ConfidenceLevel.MEDIUM,
                risk_level=RiskLevel.HIGH if abs(p.trend_pct_change) > 30 else RiskLevel.MODERATE,
                expected_impact=f"Continued decline of {p.trend_pct_change:.1f}% in {key} will compound if unaddressed",
                explanation=f"{key} has declined by {p.trend_pct_change:.1f}% (from {p.min_val if p.trend_magnitude < 0 else p.max_val:,.2f}). "
                           f"This represents a {abs(p.trend_magnitude):,.2f} unit decrease.",
                reasoning_chain=[
                    f"Sequential analysis shows {key} declining",
                    f"Total change: {p.trend_pct_change:.1f}%",
                    f"Current mean: {p.mean:,.2f}, std dev: {p.std_dev:,.2f}",
                    "Recommend root cause analysis and corrective action"
                ],
                contributing_factors=[
                    FactorContribution(factor=f"{key} trend", contribution_pct=70, direction="negative",
                                       value=p.trend_pct_change, description=f"{p.trend_pct_change:.1f}% decline"),
                    FactorContribution(factor="Volatility", contribution_pct=30, direction="negative",
                                       value=p.std_dev, description=f"Std dev of {p.std_dev:,.2f}")
                ],
                alternatives=["Increase investment in this area", "Pivot strategy", "Accept and adapt"],
                supporting_insights=[]
            ))

        return decisions

    def _correlation_decisions(self, correlations: List[CorrelationPair],
                                profiles: Dict[str, VariableProfile]) -> List[Decision]:
        """Generate decisions from strong correlations."""
        decisions = []

        strong_corrs = [c for c in correlations if c.strength == "strong"]
        if strong_corrs:
            top = strong_corrs[0]
            decisions.append(Decision(
                action=f"Leverage {top.var_a}-{top.var_b} Relationship",
                category="strategic",
                confidence=abs(top.coefficient) * 90,
                confidence_level=ConfidenceLevel.HIGH if abs(top.coefficient) > 0.8 else ConfidenceLevel.MEDIUM,
                risk_level=RiskLevel.LOW,
                expected_impact=f"Strong {top.direction} correlation (r={top.coefficient:.3f}) suggests actionable relationship",
                explanation=f"Strong {top.direction} correlation detected between {top.var_a} and {top.var_b} "
                           f"(Pearson r = {top.coefficient:.3f}). Changes in one variable predictably affect the other.",
                reasoning_chain=[
                    f"Pearson correlation: {top.coefficient:.3f}",
                    f"Classification: {top.strength} {top.direction}",
                    f"Significance: {top.significance}",
                    f"{'Increasing' if top.direction == 'positive' else 'Decreasing'} {top.var_a} will likely {'increase' if top.direction == 'positive' else 'decrease'} {top.var_b}"
                ],
                contributing_factors=[
                    FactorContribution(factor=top.var_a, contribution_pct=50, direction=top.direction,
                                       value=top.coefficient, description=f"Correlated variable"),
                    FactorContribution(factor=top.var_b, contribution_pct=50, direction=top.direction,
                                       value=top.coefficient, description=f"Correlated variable"),
                ],
                alternatives=["Monitor relationship stability", "Test causation hypothesis", "Build predictive model"],
                supporting_insights=[]
            ))

        return decisions

    def _ml_decisions(self, ml_results: List[MLModelResult],
                       profiles: Dict[str, VariableProfile]) -> List[Decision]:
        """Generate decisions from ML model outputs."""
        decisions = []

        for ml in ml_results:
            if ml.model_type == "regression" and ml.forecasts:
                last_forecast = ml.forecasts[-1]
                decisions.append(Decision(
                    action=f"Prepare for Forecasted {ml.target_variable.title()} Trajectory",
                    category="strategic",
                    confidence=min(80, ml.accuracy_value * 100 if ml.accuracy_value < 1 else ml.accuracy_value),
                    confidence_level=ConfidenceLevel.MEDIUM,
                    risk_level=RiskLevel.MODERATE,
                    expected_impact=f"Forecast predicts {ml.target_variable} reaching {last_forecast.predicted_value:,.2f}",
                    explanation=f"ML regression model (R²={ml.accuracy_value:.3f}) forecasts {ml.target_variable} "
                               f"trajectory. Next period prediction: {ml.forecasts[0].predicted_value:,.2f} "
                               f"(confidence interval: {ml.forecasts[0].lower_bound:,.2f} - {ml.forecasts[0].upper_bound:,.2f}).",
                    reasoning_chain=[
                        f"Trained linear regression model on {ml.target_variable}",
                        f"Model R² score: {ml.accuracy_value:.3f}",
                        f"Generated {len(ml.forecasts)} forecast periods",
                        f"Key features: {', '.join(f'{k}: {v:.2f}' for k, v in list(ml.feature_importance.items())[:3])}"
                    ],
                    contributing_factors=[
                        FactorContribution(factor=k, contribution_pct=v * 100, direction="positive",
                                           value=v, description=f"Feature importance: {v:.2f}")
                        for k, v in list(ml.feature_importance.items())[:3]
                    ],
                    alternatives=["Wait for more data", "Use ensemble methods", "Apply domain expertise override"],
                    supporting_insights=[]
                ))

            elif ml.model_type == "clustering":
                decisions.append(Decision(
                    action="Segment-Specific Strategy Recommended",
                    category="strategic",
                    confidence=min(75, ml.accuracy_value * 100 if ml.accuracy_value < 1 else 70),
                    confidence_level=ConfidenceLevel.MEDIUM,
                    risk_level=RiskLevel.LOW,
                    expected_impact="Data clustering reveals distinct segments that may benefit from tailored approaches",
                    explanation=f"K-Means clustering identified distinct data segments. "
                               f"Silhouette score: {ml.accuracy_value:.3f}. Consider differentiated strategies for each cluster.",
                    reasoning_chain=[
                        "Applied K-Means clustering algorithm",
                        f"Optimal cluster quality: {ml.accuracy_value:.3f}",
                        "Each cluster represents a distinct behavioral segment"
                    ],
                    contributing_factors=[
                        FactorContribution(factor=k, contribution_pct=v * 100, direction="neutral",
                                           value=v, description=f"Cluster importance: {v:.2f}")
                        for k, v in list(ml.feature_importance.items())[:3]
                    ],
                    alternatives=["Merge similar segments", "Increase cluster count", "Use hierarchical clustering"],
                    supporting_insights=[]
                ))

        return decisions

    def _generic_decision(self, profiles: Dict[str, VariableProfile],
                           numeric_keys: List[str]) -> Decision:
        """Fallback decision when no specific patterns match."""
        primary = numeric_keys[0] if numeric_keys else "data"
        p = profiles.get(primary)

        return Decision(
            action="Continue Monitoring with Enhanced Data Collection",
            category="operational",
            confidence=55,
            confidence_level=ConfidenceLevel.LOW,
            risk_level=RiskLevel.LOW,
            expected_impact="Maintain current operations while gathering more data for confident decisions",
            explanation=f"Analysis of {primary} shows standard variance with no critical signals. "
                       f"Mean: {p.mean:,.2f}, Std Dev: {p.std_dev:,.2f}. "
                       f"No urgent action required." if p else "Insufficient data for confident recommendations.",
            reasoning_chain=[
                "No critical anomalies detected",
                "No strong trend signals identified",
                "Recommend continued data collection for higher confidence",
                "Consider adding more variables for richer analysis"
            ],
            contributing_factors=[
                FactorContribution(factor="Data stability", contribution_pct=60, direction="positive",
                                   value=None, description="Values within normal ranges"),
                FactorContribution(factor="Sample size", contribution_pct=40, direction="neutral",
                                   value=None, description="More data would improve confidence"),
            ],
            alternatives=["Expand data sources", "Add temporal variables", "Set up automated monitoring"],
            supporting_insights=[]
        )

    def _rank_and_deduplicate(self, decisions: List[Decision]) -> List[Decision]:
        """Rank decisions by confidence and risk, remove duplicates."""
        # Weight: confidence * risk_weight
        risk_weights = {
            RiskLevel.SEVERE: 1.5,
            RiskLevel.HIGH: 1.3,
            RiskLevel.MODERATE: 1.0,
            RiskLevel.LOW: 0.8,
            RiskLevel.MINIMAL: 0.6,
        }

        for d in decisions:
            d.confidence = min(98, d.confidence)  # Cap at 98%

        # Sort by weighted score
        decisions.sort(key=lambda d: d.confidence * risk_weights.get(d.risk_level, 1.0), reverse=True)

        # Assign ranks
        for i, d in enumerate(decisions):
            d.rank = i + 1

        # Set confidence levels
        for d in decisions:
            if d.confidence >= 85:
                d.confidence_level = ConfidenceLevel.HIGH
            elif d.confidence >= 65:
                d.confidence_level = ConfidenceLevel.MEDIUM
            elif d.confidence >= 40:
                d.confidence_level = ConfidenceLevel.LOW
            else:
                d.confidence_level = ConfidenceLevel.LOW

        return decisions
