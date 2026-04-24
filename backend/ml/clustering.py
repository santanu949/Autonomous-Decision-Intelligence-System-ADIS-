"""
ADIS Clustering Engine - K-Means clustering for data segmentation.
Pure Python implementation.
"""
import math
import random
from typing import List, Dict, Any, Optional
from core.models import MLModelResult


class ClusteringEngine:
    """K-Means clustering for discovering natural data segments."""

    def cluster(self, data: List[Dict[str, Any]],
                numeric_keys: List[str],
                max_k: int = 5) -> Optional[MLModelResult]:
        """Perform K-Means clustering on numeric variables."""
        if len(data) < 4 or len(numeric_keys) < 2:
            return None

        # Prepare feature matrix
        matrix = []
        for row in data:
            features = [float(row.get(k, 0)) for k in numeric_keys]
            matrix.append(features)

        # Normalize features (z-score)
        normalized, means, stds = self._normalize(matrix)

        # Find optimal k using elbow method (simplified)
        best_k = min(3, len(data) // 2)
        best_k = max(2, best_k)

        # Run K-Means
        labels, centroids = self._kmeans(normalized, best_k)

        if labels is None:
            return None

        # Compute silhouette score (simplified)
        silhouette = self._silhouette_score(normalized, labels, best_k)

        # Assign cluster labels back to data
        predictions = []
        for i, row in enumerate(data):
            pred = dict(row)
            pred["_cluster"] = labels[i]
            predictions.append(pred)

        # Feature importance (variance contribution)
        feature_importance = {}
        for j, key in enumerate(numeric_keys):
            between_var = self._between_cluster_variance(normalized, labels, best_k, j)
            total_var = sum((normalized[i][j]) ** 2 for i in range(len(normalized))) / len(normalized)
            feature_importance[key] = round(between_var / max(total_var, 0.001), 4)

        return MLModelResult(
            model_type="clustering",
            target_variable="all_numeric",
            accuracy_metric="silhouette_score",
            accuracy_value=round(silhouette, 4),
            predictions=predictions,
            feature_importance=feature_importance
        )

    def _normalize(self, matrix: List[List[float]]):
        """Z-score normalization."""
        n = len(matrix)
        d = len(matrix[0])
        means = []
        stds = []

        for j in range(d):
            vals = [matrix[i][j] for i in range(n)]
            mean = sum(vals) / n
            std = math.sqrt(sum((v - mean) ** 2 for v in vals) / n)
            means.append(mean)
            stds.append(std if std > 0 else 1)

        normalized = []
        for row in matrix:
            normalized.append([(row[j] - means[j]) / stds[j] for j in range(d)])

        return normalized, means, stds

    def _kmeans(self, data: List[List[float]], k: int, max_iter: int = 50):
        """Simple K-Means clustering."""
        n = len(data)
        d = len(data[0])

        # Initialize centroids using K-Means++
        random.seed(42)
        centroids = [data[random.randint(0, n - 1)][:]]

        for _ in range(k - 1):
            distances = []
            for point in data:
                min_dist = min(self._distance(point, c) for c in centroids)
                distances.append(min_dist ** 2)

            total = sum(distances)
            if total == 0:
                centroids.append(data[random.randint(0, n - 1)][:])
                continue

            probs = [d / total for d in distances]
            r = random.random()
            cumulative = 0
            for i, p in enumerate(probs):
                cumulative += p
                if cumulative >= r:
                    centroids.append(data[i][:])
                    break

        # Iterate
        labels = [0] * n
        for iteration in range(max_iter):
            # Assign clusters
            new_labels = []
            for point in data:
                distances = [self._distance(point, c) for c in centroids]
                new_labels.append(distances.index(min(distances)))

            if new_labels == labels:
                break
            labels = new_labels

            # Update centroids
            for c in range(k):
                members = [data[i] for i in range(n) if labels[i] == c]
                if members:
                    centroids[c] = [sum(m[j] for m in members) / len(members) for j in range(d)]

        return labels, centroids

    def _distance(self, a: List[float], b: List[float]) -> float:
        return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(len(a))))

    def _silhouette_score(self, data: List[List[float]], labels: List[int], k: int) -> float:
        """Simplified silhouette score."""
        n = len(data)
        if n < 2 or k < 2:
            return 0

        scores = []
        for i in range(n):
            # a(i): mean intra-cluster distance
            same_cluster = [j for j in range(n) if labels[j] == labels[i] and j != i]
            if not same_cluster:
                scores.append(0)
                continue

            a = sum(self._distance(data[i], data[j]) for j in same_cluster) / len(same_cluster)

            # b(i): mean nearest-cluster distance
            b = float('inf')
            for c in range(k):
                if c == labels[i]:
                    continue
                other = [j for j in range(n) if labels[j] == c]
                if other:
                    mean_dist = sum(self._distance(data[i], data[j]) for j in other) / len(other)
                    b = min(b, mean_dist)

            if b == float('inf'):
                b = a

            s = (b - a) / max(a, b) if max(a, b) > 0 else 0
            scores.append(s)

        return sum(scores) / len(scores) if scores else 0

    def _between_cluster_variance(self, data: List[List[float]], labels: List[int], k: int, feature_idx: int) -> float:
        """Between-cluster variance for a single feature."""
        n = len(data)
        overall_mean = sum(data[i][feature_idx] for i in range(n)) / n

        bcv = 0
        for c in range(k):
            members = [data[i][feature_idx] for i in range(n) if labels[i] == c]
            if members:
                cluster_mean = sum(members) / len(members)
                bcv += len(members) * (cluster_mean - overall_mean) ** 2

        return bcv / n if n > 0 else 0
