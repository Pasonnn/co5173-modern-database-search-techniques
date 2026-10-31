"""Static Learned Index: Recursive Model Index (RMI) approximating CDF for static datasets."""
from __future__ import annotations
import bisect
from dataclasses import dataclass
from typing import Any
from src.common import OperationStats, estimate_object_memory


@dataclass
class LinearModel:
    slope: float = 0.0
    intercept: float = 0.0
    max_error: int = 0

    def predict(self, key: float) -> float:
        return self.slope * key + self.intercept


class StaticRMI:
    """Two-stage Recursive Model Index for immutable sorted keys.
    
    ponytail: Piecewise ordinary least squares over PyTorch neural regression; upgrade when key distributions exhibit complex multi-modal skew.
    """

    def __init__(self, num_leaf_models: int = 16):
        self.num_leaf_models = max(2, num_leaf_models)
        self.keys: list[int] = []
        self.values: list[Any] = []
        self.root_model = LinearModel()
        self.leaf_models: list[LinearModel] = []
        self.stats = OperationStats()

    def build(self, sorted_data: list[tuple[int, Any]]) -> None:
        """Trains the 2-stage hierarchy over an immutable sorted array."""
        if not sorted_data:
            return

        self.keys = [k for k, _ in sorted_data]
        self.values = [v for _, v in sorted_data]
        n = len(self.keys)

        # Stage 1: Root model maps key range -> [0, num_leaf_models - 1]
        min_k, max_k = self.keys[0], self.keys[-1]
        k_span = max(1, max_k - min_k)
        self.root_model.slope = (self.num_leaf_models - 1) / k_span
        self.root_model.intercept = -self.root_model.slope * min_k

        # Partition keys across leaf models
        leaf_buckets: list[list[tuple[int, int]]] = [[] for _ in range(self.num_leaf_models)]
        for pos, k in enumerate(self.keys):
            pred_leaf = int(self.root_model.predict(k))
            pred_leaf = max(0, min(self.num_leaf_models - 1, pred_leaf))
            leaf_buckets[pred_leaf].append((k, pos))

        # Stage 2: Train linear model for each partition with bounded error tracking
        self.leaf_models = []
        for bucket in leaf_buckets:
            model = LinearModel()
            if len(bucket) == 1:
                k, pos = bucket[0]
                model.slope = 0.0
                model.intercept = float(pos)
                model.max_error = 1
            elif len(bucket) > 1:
                # Simple OLS fit
                b_min_k, b_max_k = bucket[0][0], bucket[-1][0]
                b_min_pos, b_max_pos = bucket[0][1], bucket[-1][1]
                b_span = max(1, b_max_k - b_min_k)
                model.slope = (b_max_pos - b_min_pos) / b_span
                model.intercept = b_min_pos - model.slope * b_min_k

                # Compute maximum prediction error bound epsilon
                max_err = 0
                for k, pos in bucket:
                    err = abs(int(model.predict(k)) - pos)
                    if err > max_err:
                        max_err = err
                model.max_error = max(1, max_err)
            self.leaf_models.append(model)

    def get(self, key: int) -> Any | None:
        if not self.keys:
            return None

        # Stage 1 prediction
        leaf_idx = int(self.root_model.predict(key))
        leaf_idx = max(0, min(self.num_leaf_models - 1, leaf_idx))
        leaf_model = self.leaf_models[leaf_idx]

        # Stage 2 prediction
        pos_pred = int(leaf_model.predict(key))
        eps = leaf_model.max_error

        # Local bounded binary search within [pos_pred - eps, pos_pred + eps]
        low = max(0, pos_pred - eps)
        high = min(len(self.keys) - 1, pos_pred + eps)

        self.stats.comparisons += 1
        idx = bisect.bisect_left(self.keys, key, low, high + 1)
        if idx < len(self.keys) and self.keys[idx] == key:
            return self.values[idx]
        return None

    def scan(self, start_key: int, end_key: int) -> list[tuple[int, Any]]:
        """Fast contiguous slice after bounded point lookup of start_key."""
        idx = bisect.bisect_left(self.keys, start_key)
        results: list[tuple[int, Any]] = []
        while idx < len(self.keys) and self.keys[idx] <= end_key:
            results.append((self.keys[idx], self.values[idx]))
            idx += 1
        return results

    def memory_footprint_bytes(self) -> int:
        return estimate_object_memory(self.root_model) + estimate_object_memory(self.leaf_models)
