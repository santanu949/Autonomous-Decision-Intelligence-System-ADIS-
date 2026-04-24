"""
ADIS Anomaly Detector - Multi-method anomaly detection.
Methods: Z-score, IQR, Modified Z-score (MAD-based).
"""
import math
from typing import List, Dict, Any
from core.models import AnomalyRecord, VariableProfile, RiskLevel


class AnomalyDetector:
    """Detects statistical anomalies using multiple methods for robustness."""

    Z_THRESHOLD = 2.0
    IQR_MULTIPLIER = 1.5
    MODIFIED_Z_THRESHOLD = 3.5

    def detect(self, data: List[Dict[str, Any]],
               numeric_keys: List[str],
               profiles: Dict[str, VariableProfile]) -> List[AnomalyRecord]:
        """Run all anomaly detection methods and return unique anomalies."""
        anomalies = []

        for key in numeric_keys:
            if key not in profiles:
                continue

            values = [row.get(key, 0.0) for row in data]
            profile = profiles[key]

            if profile.std_dev is None or profile.mean is None:
                continue

            # Method 1: Z-score
            anomalies.extend(self._z_score_detect(key, values, profile))

            # Method 2: IQR
            anomalies.extend(self._iqr_detect(key, values, profile))

            # Method 3: Modified Z-score (MAD)
            anomalies.extend(self._modified_z_detect(key, values, profile))

        # Deduplicate by (variable, index)
        seen = set()
        unique = []
        for a in anomalies:
            key = (a.variable, a.index)
            if key not in seen:
                seen.add(key)
                unique.append(a)

        return sorted(unique, key=lambda x: x.deviation_score, reverse=True)

    def _z_score_detect(self, key: str, values: List[float],
                        profile: VariableProfile) -> List[AnomalyRecord]:
        anomalies = []
        if profile.std_dev == 0:
            return anomalies

        for i, val in enumerate(values):
            z = abs(val - profile.mean) / profile.std_dev
            if z > self.Z_THRESHOLD:
                anomalies.append(AnomalyRecord(
                    variable=key,
                    index=i,
                    value=round(val, 4),
                    expected_range=f"{profile.mean - 2*profile.std_dev:.2f} to {profile.mean + 2*profile.std_dev:.2f}",
                    deviation_score=round(z, 2),
                    method="z-score",
                    severity=self._severity_from_z(z),
                    context=f"Value is {z:.1f} standard deviations from the mean ({profile.mean:.2f})"
                ))
        return anomalies

    def _iqr_detect(self, key: str, values: List[float],
                    profile: VariableProfile) -> List[AnomalyRecord]:
        anomalies = []
        if profile.iqr is None or profile.q1 is None or profile.q3 is None or profile.iqr == 0:
            return anomalies

        lower = profile.q1 - self.IQR_MULTIPLIER * profile.iqr
        upper = profile.q3 + self.IQR_MULTIPLIER * profile.iqr

        for i, val in enumerate(values):
            if val < lower or val > upper:
                deviation = abs(val - profile.mean) / profile.iqr if profile.iqr > 0 else 0
                anomalies.append(AnomalyRecord(
                    variable=key,
                    index=i,
                    value=round(val, 4),
                    expected_range=f"{lower:.2f} to {upper:.2f}",
                    deviation_score=round(deviation, 2),
                    method="iqr",
                    severity=self._severity_from_z(deviation),
                    context=f"Value outside IQR fence ({lower:.2f} - {upper:.2f})"
                ))
        return anomalies

    def _modified_z_detect(self, key: str, values: List[float],
                           profile: VariableProfile) -> List[AnomalyRecord]:
        anomalies = []
        if not values or profile.median is None:
            return anomalies

        # Compute MAD (Median Absolute Deviation)
        deviations = [abs(v - profile.median) for v in values]
        mad = sorted(deviations)[len(deviations) // 2]
        if mad == 0:
            return anomalies

        for i, val in enumerate(values):
            modified_z = 0.6745 * (val - profile.median) / mad
            if abs(modified_z) > self.MODIFIED_Z_THRESHOLD:
                anomalies.append(AnomalyRecord(
                    variable=key,
                    index=i,
                    value=round(val, 4),
                    expected_range=f"MAD-based: {profile.median - 3.5*mad/0.6745:.2f} to {profile.median + 3.5*mad/0.6745:.2f}",
                    deviation_score=round(abs(modified_z), 2),
                    method="modified-z",
                    severity=self._severity_from_z(abs(modified_z)),
                    context=f"Modified Z-score: {modified_z:.2f} (robust to outliers)"
                ))
        return anomalies

    def _severity_from_z(self, z: float) -> RiskLevel:
        if z > 4:
            return RiskLevel.SEVERE
        elif z > 3:
            return RiskLevel.HIGH
        elif z > 2:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.LOW
