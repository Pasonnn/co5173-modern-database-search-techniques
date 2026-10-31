"""Shared interfaces and telemetry for database search indexing engines."""
from dataclasses import dataclass, field
import sys
from typing import Any, Protocol, runtime_checkable


@dataclass
class OperationStats:
    """Tracks I/O and amplification metrics per operation."""
    pages_read: int = 0
    pages_written: int = 0
    comparisons: int = 0
    bytes_scanned: int = 0


@runtime_checkable
class BaseIndex(Protocol):
    """Protocol for primary-key search engines."""

    def put(self, key: int, value: Any) -> None:
        ...

    def get(self, key: int) -> Any | None:
        ...

    def scan(self, start_key: int, end_key: int) -> list[tuple[int, Any]]:
        ...

    def memory_footprint_bytes(self) -> int:
        ...


def estimate_object_memory(obj: Any, seen: set[int] | None = None) -> int:
    """Recursive approximation of total memory bytes held by a Python object.
    
    ponytail: Deep Python object inspection over OS-level page allocator stats; upgrade when measuring C/Rust storage backends.
    """
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)

    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(estimate_object_memory(k, seen) + estimate_object_memory(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(estimate_object_memory(item, seen) for item in obj)
    elif hasattr(obj, "__dict__"):
        size += estimate_object_memory(vars(obj), seen)
    elif hasattr(obj, "__slots__"):
        size += sum(estimate_object_memory(getattr(obj, s), seen) for s in obj.__slots__ if hasattr(obj, s))
    return size
