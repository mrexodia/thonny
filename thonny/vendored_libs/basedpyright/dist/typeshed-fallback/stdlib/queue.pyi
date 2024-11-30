import sys
from _queue import Empty as Empty, SimpleQueue as SimpleQueue
from threading import Condition, Lock
from typing import Any, Generic, TypeVar

if sys.version_info >= (3, 9):
    from types import GenericAlias

__all__ = ["Empty", "Full", "Queue", "PriorityQueue", "LifoQueue", "SimpleQueue"]
if sys.version_info >= (3, 13):
    __all__ += ["ShutDown"]

_T = TypeVar("_T")

class Full(Exception): ...

if sys.version_info >= (3, 13):
    class ShutDown(Exception): ...

class Queue(Generic[_T]):
    maxsize: int

    mutex: Lock  # undocumented
    not_empty: Condition  # undocumented
    not_full: Condition  # undocumented
    all_tasks_done: Condition  # undocumented
    unfinished_tasks: int  # undocumented
    if sys.version_info >= (3, 13):
        is_shutdown: bool  # undocumented
    # Despite the fact that `queue` has `deque` type,
    # we treat it as `Any` to allow different implementations in subtypes.
    queue: Any  # undocumented
    def __init__(self, maxsize: int = 0) -> None: ...
    def _init(self, maxsize: int) -> None: ...
    def empty(self) -> bool: ...
    def full(self) -> bool: ...
    def get(self, block: bool = True, timeout: float | None = None) -> _T: ...
    def get_nowait(self) -> _T: ...
    if sys.version_info >= (3, 13):
        def shutdown(self, immediate: bool = False) -> None: ...

    def _get(self) -> _T: ...
    def put(self, item: _T, block: bool = True, timeout: float | None = None) -> None: ...
    def put_nowait(self, item: _T) -> None: ...
    def _put(self, item: _T) -> None: ...
    def join(self) -> None: ...
    def qsize(self) -> int: ...
    def _qsize(self) -> int: ...
    def task_done(self) -> None: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any, /) -> GenericAlias:
            """
            Represent a PEP 585 generic type

            E.g. for t = list[int], t.__origin__ is list and t.__args__ is (int,).
            """
            ...

class PriorityQueue(Queue[_T]):
    queue: list[_T]

class LifoQueue(Queue[_T]):
    queue: list[_T]
