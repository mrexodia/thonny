import sys
from _thread import _excepthook, _ExceptHookArgs
from _typeshed import ProfileFunction, TraceFunction
from collections.abc import Callable, Iterable, Mapping
from types import TracebackType
from typing import Any, TypeVar

_T = TypeVar("_T")

__all__ = [
    "get_ident",
    "active_count",
    "Condition",
    "current_thread",
    "enumerate",
    "main_thread",
    "TIMEOUT_MAX",
    "Event",
    "Lock",
    "RLock",
    "Semaphore",
    "BoundedSemaphore",
    "Thread",
    "Barrier",
    "BrokenBarrierError",
    "Timer",
    "ThreadError",
    "setprofile",
    "settrace",
    "local",
    "stack_size",
    "ExceptHookArgs",
    "excepthook",
]

def active_count() -> int: ...
def current_thread() -> Thread: ...
def currentThread() -> Thread: ...
def get_ident() -> int: ...
def enumerate() -> list[Thread]: ...
def main_thread() -> Thread: ...
def settrace(func: TraceFunction) -> None: ...
def setprofile(func: ProfileFunction | None) -> None: ...
def stack_size(size: int | None = None) -> int: ...

TIMEOUT_MAX: float

class ThreadError(Exception):
    """Unspecified run-time error."""
    ...

class local:
    def __getattribute__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __delattr__(self, name: str) -> None: ...

class Thread:
    name: str
    daemon: bool
    @property
    def ident(self) -> int | None:
        """
        Thread identifier of this thread or None if it has not been started.

        This is a nonzero integer. See the get_ident() function. Thread
        identifiers may be recycled when a thread exits and another thread is
        created. The identifier is available even after the thread has exited.
        """
        ...
    def __init__(
        self,
        group: None = None,
        target: Callable[..., object] | None = None,
        name: str | None = None,
        args: Iterable[Any] = (),
        kwargs: Mapping[str, Any] | None = None,
        *,
        daemon: bool | None = None,
    ) -> None: ...
    def start(self) -> None: ...
    def run(self) -> None: ...
    def join(self, timeout: float | None = None) -> None: ...
    def getName(self) -> str: ...
    def setName(self, name: str) -> None: ...
    @property
    def native_id(self) -> int | None: ...  # only available on some platforms
    def is_alive(self) -> bool: ...
    if sys.version_info < (3, 9):
        def isAlive(self) -> bool: ...

    def isDaemon(self) -> bool: ...
    def setDaemon(self, daemonic: bool) -> None: ...

class _DummyThread(Thread): ...

class Lock:
    def __enter__(self) -> bool: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> bool | None: ...
    def acquire(self, blocking: bool = ..., timeout: float = ...) -> bool: ...
    def release(self) -> None: ...
    def locked(self) -> bool: ...

class _RLock:
    def __enter__(self) -> bool: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> bool | None: ...
    def acquire(self, blocking: bool = True, timeout: float = -1) -> bool: ...
    def release(self) -> None: ...

RLock = _RLock

class Condition:
    def __init__(self, lock: Lock | _RLock | None = None) -> None: ...
    def __enter__(self) -> bool: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> bool | None: ...
    def acquire(self, blocking: bool = ..., timeout: float = ...) -> bool: ...
    def release(self) -> None: ...
    def wait(self, timeout: float | None = None) -> bool: ...
    def wait_for(self, predicate: Callable[[], _T], timeout: float | None = None) -> _T: ...
    def notify(self, n: int = 1) -> None: ...
    def notify_all(self) -> None: ...
    def notifyAll(self) -> None: ...

class Semaphore:
    def __init__(self, value: int = 1) -> None: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> bool | None: ...
    def acquire(self, blocking: bool = True, timeout: float | None = None) -> bool: ...
    def __enter__(self, blocking: bool = True, timeout: float | None = None) -> bool: ...
    if sys.version_info >= (3, 9):
        def release(self, n: int = ...) -> None: ...
    else:
        def release(self) -> None: ...

class BoundedSemaphore(Semaphore): ...

class Event:
    def is_set(self) -> bool: ...
    def set(self) -> None: ...
    def clear(self) -> None: ...
    def wait(self, timeout: float | None = None) -> bool: ...

excepthook = _excepthook
ExceptHookArgs = _ExceptHookArgs

class Timer(Thread):
    def __init__(
        self,
        interval: float,
        function: Callable[..., object],
        args: Iterable[Any] | None = None,
        kwargs: Mapping[str, Any] | None = None,
    ) -> None: ...
    def cancel(self) -> None: ...

class Barrier:
    @property
    def parties(self) -> int:
        """Return the number of threads required to trip the barrier."""
        ...
    @property
    def n_waiting(self) -> int:
        """Return the number of threads currently waiting at the barrier."""
        ...
    @property
    def broken(self) -> bool:
        """Return True if the barrier is in a broken state."""
        ...
    def __init__(self, parties: int, action: Callable[[], None] | None = None, timeout: float | None = None) -> None: ...
    def wait(self, timeout: float | None = None) -> int: ...
    def reset(self) -> None: ...
    def abort(self) -> None: ...

class BrokenBarrierError(RuntimeError): ...
