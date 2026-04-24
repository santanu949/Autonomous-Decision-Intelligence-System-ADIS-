"""
ADIS Explainability Engine - Generates human-readable explanations for every decision.
Dual-level: Executive summary + Technical detail.
"""
from typing import List, Dict, Any
from core.models import (
    Decision, Insight, VariableProfile, AnomalyRecord, CorrelationPair
)


class ExplainabilityEngine:
    """
    Enhances decisions with detailed, data-grounded explanations.
    Every decision gets:
    - Executive summary (1-2 sentences)
    - Technical detail (full breakdown)
    - Factor contributions with percentages
    """

    def enhance(self, decisions: List[Decision],
                insights: List[Insight],
                profiles: Dict[str, VariableProfile],
                anomalies: List[AnomalyRecord],
                correlations: List[CorrelationPair]) -> List[Decision]:
        """Enhance all decisions with rich explanations."""
        for decision in decisions:
            decision.executive_summary = self._generate_executive_summary(decision)
            decision.technical_detail = self._generate_technical_detail(
                decision, insights, profiles, anomalies, correlations
            )
            # Link supporting insights
            decision.supporting_insights = self._find_supporting_insights(decision, insights)

        return decisions

    def _generate_executive_summary(self, decision: Decision) -> str:
        """1-2 sentence executive-level summary."""
        confidence_word = {
            "high": "strongly recommend",
            "medium": "recommend",
            "low": "suggest considering",
            "critical": "urgently recommend"
        }.get(decision.confidence_level.value, "recommend")

        risk_word = {
            "severe": "with critical urgency",
            "high": "as a high priority",
            "moderate": "at your earliest convenience",
            "low": "when resources permit",
            "minimal": "as a low-priority optimization"
        }.get(decision.risk_level.value, "")

        return (f"We {confidence_word} \"{decision.action}\" {risk_word}. "
                f"Confidence: {decision.confidence:.0f}%. {decision.expected_impact}.")

    def _generate_technical_detail(self, decision: Decision,
                                    insights: List[Insight],
                                    profiles: Dict[str, VariableProfile],
                                    anomalies: List[AnomalyRecord],
                                    correlations: List[CorrelationPair]) -> str:
        """Detailed technical breakdown."""
        parts = []

        # Reasoning chain
        if decision.reasoning_chain:
            parts.append("**Reasoning Chain:**")
            for i, step in enumerate(decision.reasoning_chain, 1):
                parts.append(f"  {i}. {step}")

        # Contributing factors
        if decision.contributing_factors:
            parts.append("\n**Factor Breakdown:**")
            for factor in decision.contributing_factors:
                arrow = "↑" if factor.direction == "positive" else ("↓" if factor.direction == "negative" else "→")
                parts.append(f"  {arrow} {factor.factor}: {factor.contribution_pct:.0f}% — {factor.description}")

        # Related anomalies
        related_anomalies = [a for a in anomalies
                             if any(f.factor.lower().find(a.variable.lower()) >= 0
                                    for f in decision.contributing_factors)]
        if related_anomalies:
            parts.append(f"\n**Related Anomalies:** {len(related_anomalies)} detected")
            for a in related_anomalies[:3]:
                parts.append(f"  ⚠ {a.variable}[{a.index}] = {a.value} (expected: {a.expected_range})")

        # Related correlations
        factor_vars = set()
        for f in decision.contributing_factors:
            factor_vars.add(f.factor.split()[0].lower())

        related_corrs = [c for c in correlations
                         if c.var_a.lower() in factor_vars or c.var_b.lower() in factor_vars]
        if related_corrs:
            parts.append(f"\n**Related Correlations:**")
            for c in related_corrs[:3]:
                parts.append(f"  🔗 {c.var_a} ↔ {c.var_b}: r={c.coefficient:.3f} ({c.strength})")

        # Alternatives
        if decision.alternatives:
            parts.append(f"\n**Alternative Actions:** {', '.join(decision.alternatives)}")

        return "\n".join(parts) if parts else decision.explanation

    def _find_supporting_insights(self, decision: Decision,
                                   insights: List[Insight]) -> List[str]:
        """Find insight IDs that support this decision."""
        supporting = []
        decision_vars = set()
        for f in decision.contributing_factors:
            # Extract variable names from factor descriptions
            for word in f.factor.lower().split():
                if len(word) > 2:
                    decision_vars.add(word)

        for insight in insights:
            for factor in insight.contributing_factors:
                if factor.lower() in decision_vars:
                    supporting.append(insight.id)
                    break

        return supporting[:5]
