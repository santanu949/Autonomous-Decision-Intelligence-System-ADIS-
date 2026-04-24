"""
ADIS Data Models - Pydantic models for type-safe data flow through the pipeline.
Every decision, insight, and analysis result is a structured, validated object.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from enum import Enum
import uuid


class VariableType(str, Enum):
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    TEMPORAL = "temporal"
    TEXT = "text"
    BOOLEAN = "boolean"


class ConfidenceLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RiskLevel(str, Enum):
    SEVERE = "severe"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    MINIMAL = "minimal"


class VariableProfile(BaseModel):
    """Statistical profile of a single variable/column."""
    name: str
    var_type: VariableType
    count: int = 0
    missing: int = 0
    unique: int = 0
    # Numeric stats
    mean: Optional[float] = None
    median: Optional[float] = None
    std_dev: Optional[float] = None
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    q1: Optional[float] = None
    q3: Optional[float] = None
    iqr: Optional[float] = None
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None
    # Trend
    trend_direction: Optional[str] = None
    trend_magnitude: Optional[float] = None
    trend_pct_change: Optional[float] = None
    # Categorical stats
    top_values: Optional[Dict[str, int]] = None


class AnomalyRecord(BaseModel):
    """A detected anomaly in the data."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    variable: str
    index: int
    value: float
    expected_range: str
    deviation_score: float
    method: str  # z-score, iqr, modified-z
    severity: RiskLevel
    context: Optional[str] = None


class CorrelationPair(BaseModel):
    """Correlation between two variables."""
    var_a: str
    var_b: str
    coefficient: float
    strength: str  # strong, moderate, weak, negligible
    direction: str  # positive, negative
    significance: str  # significant, not_significant


class Insight(BaseModel):
    """A data-driven insight extracted from analysis."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    category: str  # trend, anomaly, correlation, distribution, pattern
    title: str
    description: str
    severity: str = "info"  # info, warning, critical
    confidence: float = 0.0  # 0-100
    contributing_factors: List[str] = []
    data_evidence: Optional[Dict[str, Any]] = None


class FactorContribution(BaseModel):
    """How much a factor contributed to a decision."""
    factor: str
    contribution_pct: float
    direction: str  # positive, negative, neutral
    value: Optional[Any] = None
    description: str


class Decision(BaseModel):
    """A ranked, explainable decision/recommendation."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    rank: int = 1
    action: str
    category: str = "general"  # growth, cost, risk, operational, strategic
    confidence: float = 0.0  # 0-100 numeric
    confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM
    risk_level: RiskLevel = RiskLevel.MODERATE
    expected_impact: str = ""
    explanation: str = ""
    executive_summary: str = ""
    technical_detail: str = ""
    reasoning_chain: List[str] = []
    contributing_factors: List[FactorContribution] = []
    alternatives: List[str] = []
    supporting_insights: List[str] = []  # insight IDs


class ForecastPoint(BaseModel):
    """A single forecast data point."""
    period: str
    predicted_value: float
    lower_bound: float
    upper_bound: float
    confidence: float


class MLModelResult(BaseModel):
    """Result from an ML model run."""
    model_type: str  # regression, classification, clustering
    target_variable: str
    accuracy_metric: str
    accuracy_value: float
    predictions: List[Dict[str, Any]] = []
    feature_importance: Dict[str, float] = {}
    forecasts: List[ForecastPoint] = []


class DataProfile(BaseModel):
    """Complete profile of the ingested dataset."""
    row_count: int
    column_count: int
    variables: List[VariableProfile] = []
    quality_score: float = 0.0  # 0-100
    completeness: float = 0.0  # 0-100
    issues: List[str] = []


class ScenarioResult(BaseModel):
    """Result of a what-if scenario simulation."""
    scenario_name: str
    adjustments: Dict[str, float]
    baseline_decisions: List[Decision] = []
    adjusted_decisions: List[Decision] = []
    impact_summary: str = ""
    sensitivity: Dict[str, float] = {}


class AuditEntry(BaseModel):
    """Audit trail entry for traceability."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    stage: str  # ingestion, validation, analysis, decision, ml
    action: str
    details: Dict[str, Any] = {}
    duration_ms: Optional[float] = None


class AnalysisResult(BaseModel):
    """Complete output from the ADIS pipeline."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # Data profile
    data_profile: DataProfile
    # Core outputs
    decisions: List[Decision] = []
    insights: List[Insight] = []
    anomalies: List[AnomalyRecord] = []
    correlations: List[CorrelationPair] = []
    # ML outputs
    ml_results: List[MLModelResult] = []
    # Visualization data
    chart_data: List[Dict[str, Any]] = []
    variable_profiles: Dict[str, Dict[str, Any]] = {}
    # Audit
    audit_trail: List[AuditEntry] = []
    # Performance
    total_processing_ms: float = 0.0
    pipeline_stages: Dict[str, float] = {}
