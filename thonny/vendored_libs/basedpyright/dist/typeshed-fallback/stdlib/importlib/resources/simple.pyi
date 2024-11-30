import abc
import sys
from collections.abc import Iterator
from io import TextIOWrapper
from typing import IO, Any, BinaryIO, Literal, NoReturn, overload
from typing_extensions import Never

if sys.version_info >= (3, 11):
    from .abc import Traversable, TraversableResources

    class SimpleReader(abc.ABC):
        @property
        @abc.abstractmethod
        def package(self) -> str:
            """The name of the package for which this reader loads resources."""
            ...
        @abc.abstractmethod
        def children(self) -> list[SimpleReader]: ...
        @abc.abstractmethod
        def resources(self) -> list[str]: ...
        @abc.abstractmethod
        def open_binary(self, resource: str) -> BinaryIO: ...
        @property
        def name(self) -> str: ...

    class ResourceHandle(Traversable, metaclass=abc.ABCMeta):
        parent: ResourceContainer
        def __init__(self, parent: ResourceContainer, name: str) -> None: ...
        def is_file(self) -> Literal[True]: ...
        def is_dir(self) -> Literal[False]: ...
        @overload
        def open(
            self,
            mode: Literal["r"] = "r",
            encoding: str | None = None,
            errors: str | None = None,
            newline: str | None = None,
            line_buffering: bool = False,
            write_through: bool = False,
        ) -> TextIOWrapper: ...
        @overload
        def open(self, mode: Literal["rb"]) -> BinaryIO: ...
        @overload
        def open(self, mode: str) -> IO[Any]: ...
        def joinpath(self, name: Never) -> NoReturn: ...  # type: ignore[override]

    class ResourceContainer(Traversable, metaclass=abc.ABCMeta):
        reader: SimpleReader
        def __init__(self, reader: SimpleReader) -> None: ...
        def is_dir(self) -> Literal[True]: ...
        def is_file(self) -> Literal[False]: ...
        def iterdir(self) -> Iterator[ResourceHandle | ResourceContainer]: ...
        def open(self, *args: Never, **kwargs: Never) -> NoReturn: ...  # type: ignore[override]
        if sys.version_info < (3, 12):
            def joinpath(self, *descendants: str) -> Traversable: ...

    class TraversableReader(TraversableResources, SimpleReader, metaclass=abc.ABCMeta):
        def files(self) -> ResourceContainer: ...
