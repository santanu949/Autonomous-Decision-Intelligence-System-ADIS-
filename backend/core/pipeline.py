"""
ADIS Pipeline Orchestrator - Coordinates the full data-to-decision pipeline.
Each stage is independently testable, extensible, and monitored.
"""
import time
import logging
from typing import List, Dict, Any, Optional

from core.models import (
    AnalysisResult, DataProfile, AuditEntry, ScenarioResult, Insight
)
from ingestion.parser import AdaptiveParser
from analytics.statistical import StatisticalEngine
from analytics.anomaly import AnomalyDetector
from analytics.correlation import CorrelationAnalyzer
from analytics.trends import TrendAnalyzer
from decisions.synthesizer import DecisionSynthesizer
from explainability.engine import ExplainabilityEngine
from ml.forecasting import ForecastingEngine
from ml.clustering import ClusteringEngine

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """
    Orchestrates the full ADIS pipeline:
    Raw Input → Validation → Normalization → Feature Extraction →
    Analysis → Decision Synthesis → Explanation → Presentation
    """

    def __init__(self):
        self.parser = AdaptiveParser()
        self.stats_engine = StatisticalEngine()
        self.anomaly_detector = AnomalyDetector()
        self.correlation_analyzer = CorrelationAnalyzer()
        self.trend_analyzer = TrendAnalyzer()
        self.decision_synthesizer = DecisionSynthesizer()
        self.explainability_engine = ExplainabilityEngine()
        self.forecasting_engine = ForecastingEngine()
        self.clustering_engine = ClusteringEngine()
        self.audit_trail: List[AuditEntry] = []
        self._last_result: Optional[AnalysisResult] = None

    def _audit(self, stage: str, action: str, details: Dict[str, Any] = None, duration_ms: float = None):
        entry = AuditEntry(
            stage=stage,
            action=action,
            details=details or {},
            duration_ms=duration_ms
        )
        self.audit_trail.append(entry)

    def process(self, raw_data: List[Dict[str, Any]], enable_ml: bool = True) -> AnalysisResult:
        """Execute the full pipeline and return structured results."""
        pipeline_start = time.time()
        stage_timings = {}

        # ── Stage 1: Ingestion & Validation ──
        t0 = time.time()
        parsed = self.parser.parse(raw_data)
        validated_data = parsed["data"]
        data_profile = parsed["profile"]
        numeric_keys = parsed["numeric_keys"]
        categorical_keys = parsed["categorical_keys"]
        temporal_keys = parsed["temporal_keys"]
        stage_timings["ingestion"] = round((time.time() - t0) * 1000, 2)
        self._audit("ingestion", "Data parsed and validated", {
            "rows": data_profile.row_count,
            "columns": data_profile.column_count,
            "quality_score": data_profile.quality_score
        }, stage_timings["ingestion"])

        # ── Stage 2: Statistical Analysis ──
        t0 = time.time()
        variable_profiles = self.stats_engine.analyze(validated_data, numeric_keys, categorical_keys)
        stage_timings["statistics"] = round((time.time() - t0) * 1000, 2)
        self._audit("analysis", "Statistical profiling complete", {
            "variables_analyzed": len(variable_profiles)
        }, stage_timings["statistics"])

        # ── Stage 3: Anomaly Detection ──
        t0 = time.time()
        anomalies = self.anomaly_detector.detect(validated_data, numeric_keys, variable_profiles)
        stage_timings["anomaly_detection"] = round((time.time() - t0) * 1000, 2)
        self._audit("analysis", "Anomaly detection complete", {
            "anomalies_found": len(anomalies)
        }, stage_timings["anomaly_detection"])

        # ── Stage 4: Correlation Analysis ──
        t0 = time.time()
        correlations = self.correlation_analyzer.analyze(validated_data, numeric_keys)
        stage_timings["correlation"] = round((time.time() - t0) * 1000, 2)
        self._audit("analysis", "Correlation analysis complete", {
            "pairs_analyzed": len(correlations)
        }, stage_timings["correlation"])

        # ── Stage 5: Trend Analysis ──
        t0 = time.time()
        trend_insights = self.trend_analyzer.analyze(validated_data, numeric_keys, variable_profiles, categorical_keys)
        stage_timings["trends"] = round((time.time() - t0) * 1000, 2)
        self._audit("analysis", "Trend analysis complete", {
            "trends_found": len(trend_insights)
        }, stage_timings["trends"])

        # ── Stage 6: ML Models (optional) ──
        ml_results = []
        if enable_ml and len(validated_data) >= 3:
            t0 = time.time()
            try:
                forecasts = self.forecasting_engine.forecast(validated_data, numeric_keys)
                ml_results.extend(forecasts)
            except Exception as e:
                logger.warning(f"Forecasting failed: {e}")

            try:
                clusters = self.clustering_engine.cluster(validated_data, numeric_keys)
                if clusters:
                    ml_results.append(clusters)
            except Exception as e:
                logger.warning(f"Clustering failed: {e}")

            stage_timings["ml"] = round((time.time() - t0) * 1000, 2)
            self._audit("ml", "ML models executed", {
                "models_run": len(ml_results)
            }, stage_timings.get("ml", 0))

        # ── Stage 7: Decision Synthesis ──
        t0 = time.time()
        all_insights = trend_insights  # combine all insights
        # Add anomaly-derived insights
        for anom in anomalies:
            all_insights.append(Insight(
                category="anomaly",
                title=f"Anomaly in {anom.variable}",
                description=f"Value {anom.value} at index {anom.index} deviates significantly ({anom.method}: {anom.deviation_score:.1f}σ)",
                severity="warning" if anom.severity.value in ["moderate", "high"] else "critical",
                confidence=min(95, abs(anom.deviation_score) * 20),
                contributing_factors=[anom.variable],
                data_evidence={"value": anom.value, "expected_range": anom.expected_range}
            ))

        # Add correlation-derived insights
        for corr in correlations:
            if corr.strength in ["strong", "moderate"]:
                all_insights.append(Insight(
                    category="correlation",
                    title=f"{corr.strength.title()} {corr.direction} correlation: {corr.var_a} ↔ {corr.var_b}",
                    description=f"Pearson coefficient of {corr.coefficient:.3f} indicates a {corr.strength} {corr.direction} relationship between {corr.var_a} and {corr.var_b}.",
                    severity="info",
                    confidence=abs(corr.coefficient) * 100,
                    contributing_factors=[corr.var_a, corr.var_b]
                ))

        decisions = self.decision_synthesizer.synthesize(
            validated_data, variable_profiles, all_insights,
            anomalies, correlations, ml_results,
            numeric_keys, categorical_keys
        )
        stage_timings["decision_synthesis"] = round((time.time() - t0) * 1000, 2)
        self._audit("decision", "Decision synthesis complete", {
            "decisions_generated": len(decisions)
        }, stage_timings["decision_synthesis"])

        # ── Stage 8: Explainability Enhancement ──
        t0 = time.time()
        decisions = self.explainability_engine.enhance(
            decisions, all_insights, variable_profiles, anomalies, correlations
        )
        stage_timings["explainability"] = round((time.time() - t0) * 1000, 2)
        self._audit("explanation", "Explainability applied", {
            "decisions_explained": len(decisions)
        }, stage_timings["explainability"])

        total_ms = round((time.time() - pipeline_start) * 1000, 2)

        # ── Build result ──
        # Serialize variable profiles for JSON
        var_profiles_dict = {}
        for key, vp in variable_profiles.items():
            var_profiles_dict[key] = vp.model_dump() if hasattr(vp, 'model_dump') else vp

        result = AnalysisResult(
            data_profile=data_profile,
            decisions=decisions,
            insights=all_insights,
            anomalies=anomalies,
            correlations=correlations,
            ml_results=ml_results,
            chart_data=validated_data,
            variable_profiles=var_profiles_dict,
            audit_trail=self.audit_trail,
            total_processing_ms=total_ms,
            pipeline_stages=stage_timings
        )

        self._last_result = result
        self.audit_trail = []  # Reset for next run
        return result

    def simulate_scenario(self, raw_data: List[Dict[str, Any]],
                          adjustments: Dict[str, float],
                          scenario_name: str = "Custom Scenario") -> ScenarioResult:
        """Run what-if analysis by adjusting variables and re-running the pipeline."""
        # Get baseline
        baseline = self.process(raw_data, enable_ml=False)

        # Apply adjustments
        adjusted_data = []
        for row in raw_data:
            new_row = dict(row)
            for var, multiplier in adjustments.items():
                if var in new_row and isinstance(new_row[var], (int, float)):
                    new_row[var] = new_row[var] * multiplier
            adjusted_data.append(new_row)

        # Run adjusted analysis
        adjusted_result = self.process(adjusted_data, enable_ml=False)

        # Compute sensitivity
        sensitivity = {}
        for var, multiplier in adjustments.items():
            if baseline.decisions and adjusted_result.decisions:
                baseline_conf = baseline.decisions[0].confidence
                adjusted_conf = adjusted_result.decisions[0].confidence
                sensitivity[var] = round(adjusted_conf - baseline_conf, 2)

        return ScenarioResult(
            scenario_name=scenario_name,
            adjustments=adjustments,
            baseline_decisions=baseline.decisions,
            adjusted_decisions=adjusted_result.decisions,
            impact_summary=f"Adjusting {', '.join(adjustments.keys())} resulted in {len(adjusted_result.decisions)} revised decisions.",
            sensitivity=sensitivity
        )

    def get_last_result(self) -> Optional[AnalysisResult]:
        return self._last_result

    def generate_chat_response(self, query: str) -> str:
        """Generate context-aware chat response based on latest analysis."""
        query_lower = query.lower()
        result = self._last_result

        if not result:
            return "No analysis data available yet. Please run an analysis first by submitting data through the dashboard."

        # Decision-related queries
        if any(w in query_lower for w in ["decision", "recommend", "action", "what should"]):
            if result.decisions:
                top = result.decisions[0]
                return (f"**Top Recommendation:** {top.action}\n\n"
                        f"**Confidence:** {top.confidence:.0f}%\n\n"
                        f"**Reasoning:** {top.explanation}\n\n"
                        f"**Key Factors:**\n" +
                        "\n".join(f"- {f.factor}: {f.contribution_pct:.0f}% ({f.direction})" for f in top.contributing_factors[:3]))

        # Trend queries
        if any(w in query_lower for w in ["trend", "forecast", "predict", "future", "growth"]):
            trend_insights = [i for i in result.insights if i.category == "trend"]
            if trend_insights:
                return "**Trend Analysis:**\n\n" + "\n".join(f"• {t.description}" for t in trend_insights[:3])
            if result.ml_results:
                for ml in result.ml_results:
                    if ml.model_type == "regression" and ml.forecasts:
                        return ("**Forecast Results:**\n\n" +
                                "\n".join(f"• {f.period}: {f.predicted_value:.2f} (±{f.upper_bound - f.predicted_value:.2f})"
                                          for f in ml.forecasts[:3]))

        # Anomaly queries
        if any(w in query_lower for w in ["anomaly", "anomalies", "outlier", "unusual", "risk", "warning"]):
            if result.anomalies:
                return (f"**{len(result.anomalies)} Anomalies Detected:**\n\n" +
                        "\n".join(f"• **{a.variable}** at index {a.index}: value {a.value} "
                                  f"(expected {a.expected_range}, severity: {a.severity.value})"
                                  for a in result.anomalies[:5]))
            return "No anomalies detected in the current dataset. All values are within expected ranges."

        # Correlation queries
        if any(w in query_lower for w in ["correlation", "relationship", "related", "connected"]):
            strong = [c for c in result.correlations if c.strength in ["strong", "moderate"]]
            if strong:
                return ("**Key Correlations:**\n\n" +
                        "\n".join(f"• {c.var_a} ↔ {c.var_b}: {c.coefficient:.3f} ({c.strength} {c.direction})"
                                  for c in strong[:5]))

        # Data quality queries
        if any(w in query_lower for w in ["quality", "data", "profile", "summary", "overview"]):
            dp = result.data_profile
            return (f"**Data Profile:**\n\n"
                    f"• Rows: {dp.row_count}, Columns: {dp.column_count}\n"
                    f"• Quality Score: {dp.quality_score:.0f}/100\n"
                    f"• Completeness: {dp.completeness:.0f}%\n"
                    f"• Variables: {', '.join(v.name for v in dp.variables[:5])}")

        # Performance queries
        if any(w in query_lower for w in ["performance", "speed", "time", "latency"]):
            return (f"**Pipeline Performance:**\n\n"
                    f"• Total processing: {result.total_processing_ms:.0f}ms\n" +
                    "\n".join(f"• {stage}: {ms:.0f}ms" for stage, ms in result.pipeline_stages.items()))

        # General fallback with actual data
        return (f"Based on analysis of {result.data_profile.row_count} records:\n\n"
                f"• **{len(result.decisions)} decisions** generated\n"
                f"• **{len(result.insights)} insights** discovered\n"
                f"• **{len(result.anomalies)} anomalies** detected\n"
                f"• Top recommendation: {result.decisions[0].action if result.decisions else 'N/A'}\n\n"
                f"Ask me about specific decisions, trends, anomalies, or correlations for deeper analysis.")
