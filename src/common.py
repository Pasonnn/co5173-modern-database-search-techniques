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
    """Iterative approximation of total memory bytes held by an object graph.
    
    ponytail: Iterative object traversal over OS-level page allocator stats; upgrade when measuring C/Rust storage backends.
    """
    if seen is None:
        seen = set()

    total_size = 0
    stack = [obj]

    while stack:
        curr = stack.pop()
        curr_id = id(curr)
        if curr_id in seen:
            continue
        seen.add(curr_id)

        total_size += sys.getsizeof(curr)

        if isinstance(curr, dict):
            for k, v in curr.items():
                stack.append(k)
                stack.append(v)
        elif isinstance(curr, (list, tuple, set, frozenset)):
            stack.extend(curr)
        elif hasattr(curr, "__dict__"):
            stack.append(vars(curr))
        elif hasattr(curr, "__slots__"):
            for s in curr.__slots__:
                if hasattr(curr, s):
                    stack.append(getattr(curr, s))

    return total_size
