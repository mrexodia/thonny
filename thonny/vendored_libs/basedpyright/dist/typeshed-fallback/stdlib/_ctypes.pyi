"""Create and manipulate C compatible data types in Python."""

import sys
from _typeshed import ReadableBuffer, WriteableBuffer
from abc import abstractmethod
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from ctypes import CDLL, ArgumentError as ArgumentError, c_void_p
from typing import Any, ClassVar, Generic, TypeVar, overload
from typing_extensions import Self, TypeAlias

if sys.version_info >= (3, 9):
    from types import GenericAlias

_T = TypeVar("_T")
_CT = TypeVar("_CT", bound=_CData)

FUNCFLAG_CDECL: int
FUNCFLAG_PYTHONAPI: int
FUNCFLAG_USE_ERRNO: int
FUNCFLAG_USE_LASTERROR: int
RTLD_GLOBAL: int
RTLD_LOCAL: int

if sys.version_info >= (3, 11):
    CTYPES_MAX_ARGCOUNT: int

if sys.version_info >= (3, 12):
    SIZEOF_TIME_T: int

if sys.platform == "win32":
    # Description, Source, HelpFile, HelpContext, scode
    _COMError_Details: TypeAlias = tuple[str | None, str | None, str | None, int | None, int | None]

    class COMError(Exception):
        hresult: int
        text: str | None
        details: _COMError_Details

        def __init__(self, hresult: int, text: str | None, details: _COMError_Details) -> None: ...

    def CopyComPointer(src: _PointerLike, dst: _PointerLike | _CArgObject) -> int: ...

    FUNCFLAG_HRESULT: int
    FUNCFLAG_STDCALL: int

    def FormatError(code: int = ...) -> str: ...
    def get_last_error() -> int: ...
    def set_last_error(value: int) -> int: ...
    def LoadLibrary(name: str, load_flags: int = 0, /) -> int: ...
    def FreeLibrary(handle: int, /) -> None: ...

class _CDataMeta(type):
    # By default mypy complains about the following two methods, because strictly speaking cls
    # might not be a Type[_CT]. However this can never actually happen, because the only class that
    # uses _CDataMeta as its metaclass is _CData. So it's safe to ignore the errors here.
    def __mul__(cls: type[_CT], other: int) -> type[Array[_CT]]: ...  # type: ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]
    def __rmul__(cls: type[_CT], other: int) -> type[Array[_CT]]: ...  # type: ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]

class _CData(metaclass=_CDataMeta):
    _b_base_: int
    _b_needsfree_: bool
    _objects: Mapping[Any, int] | None
    # At runtime the following classmethods are available only on classes, not
    # on instances. This can't be reflected properly in the type system:
    #
    # Structure.from_buffer(...)  # valid at runtime
    # Structure(...).from_buffer(...)  # invalid at runtime
    #
    @classmethod
    def from_buffer(cls, source: WriteableBuffer, offset: int = ...) -> Self: ...
    @classmethod
    def from_buffer_copy(cls, source: ReadableBuffer, offset: int = ...) -> Self: ...
    @classmethod
    def from_address(cls, address: int) -> Self: ...
    @classmethod
    def from_param(cls, value: Any, /) -> Self | _CArgObject: ...
    @classmethod
    def in_dll(cls, library: CDLL, name: str) -> Self: ...
    def __buffer__(self, flags: int, /) -> memoryview: ...
    def __release_buffer__(self, buffer: memoryview, /) -> None: ...

class _SimpleCData(_CData, Generic[_T]):
    """XXX to be provided"""
    value: _T
    # The TypeVar can be unsolved here,
    # but we can't use overloads without creating many, many mypy false-positive errors
    def __init__(self, value: _T = ...) -> None: ...  # pyright: ignore[reportInvalidTypeVarUse]

class _CanCastTo(_CData): ...
class _PointerLike(_CanCastTo): ...

class _Pointer(_PointerLike, _CData, Generic[_CT]):
    """XXX to be provided"""
    _type_: type[_CT]
    contents: _CT
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, arg: _CT) -> None: ...
    @overload
    def __getitem__(self, key: int, /) -> Any:
        """Return self[key]."""
        ...
    @overload
    def __getitem__(self, key: slice, /) -> list[Any]:
        """Return self[key]."""
        ...
    def __setitem__(self, key: int, value: Any, /) -> None:
        """Set self[key] to value."""
        ...

@overload
def POINTER(type: None, /) -> type[c_void_p]:
    """
    Create and return a new ctypes pointer type.

      type
        A ctypes type.

    Pointer types are cached and reused internally,
    so calling this function repeatedly is cheap.
    """
    ...
@overload
def POINTER(type: type[_CT], /) -> type[_Pointer[_CT]]:
    """
    Create and return a new ctypes pointer type.

      type
        A ctypes type.

    Pointer types are cached and reused internally,
    so calling this function repeatedly is cheap.
    """
    ...
def pointer(obj: _CT, /) -> _Pointer[_CT]:
    """
    Create a new pointer instance, pointing to 'obj'.

    The returned object is of the type POINTER(type(obj)). Note that if you
    just want to pass a pointer to an object to a foreign function call, you
    should use byref(obj) which is much faster.
    """
    ...

class _CArgObject: ...

def byref(obj: _CData, offset: int = ...) -> _CArgObject:
    """
    byref(C instance[, offset=0]) -> byref-object
    Return a pointer lookalike to a C instance, only usable
    as function argument
    """
    ...

_ECT: TypeAlias = Callable[[_CData | None, CFuncPtr, tuple[_CData, ...]], _CData]
_PF: TypeAlias = tuple[int] | tuple[int, str | None] | tuple[int, str | None, Any]

class CFuncPtr(_PointerLike, _CData):
    """Function Pointer"""
    restype: type[_CData] | Callable[[int], Any] | None
    argtypes: Sequence[type[_CData]]
    errcheck: _ECT
    # Abstract attribute that must be defined on subclasses
    _flags_: ClassVar[int]
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, address: int, /) -> None: ...
    @overload
    def __init__(self, callable: Callable[..., Any], /) -> None: ...
    @overload
    def __init__(self, func_spec: tuple[str | int, CDLL], paramflags: tuple[_PF, ...] | None = ..., /) -> None: ...
    if sys.platform == "win32":
        @overload
        def __init__(
            self, vtbl_index: int, name: str, paramflags: tuple[_PF, ...] | None = ..., iid: _CData | None = ..., /
        ) -> None: ...

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call self as a function."""
        ...

_GetT = TypeVar("_GetT")
_SetT = TypeVar("_SetT")

class _CField(Generic[_CT, _GetT, _SetT]):
    offset: int
    size: int
    @overload
    def __get__(self, instance: None, owner: type[Any] | None, /) -> Self: ...
    @overload
    def __get__(self, instance: Any, owner: type[Any] | None, /) -> _GetT: ...
    def __set__(self, instance: Any, value: _SetT, /) -> None: ...

class _StructUnionMeta(_CDataMeta):
    _fields_: Sequence[tuple[str, type[_CData]] | tuple[str, type[_CData], int]]
    _pack_: int
    _anonymous_: Sequence[str]
    def __getattr__(self, name: str) -> _CField[Any, Any, Any]: ...

class _StructUnionBase(_CData, metaclass=_StructUnionMeta):
    def __init__(self, *args: Any, **kw: Any) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...

class Union(_StructUnionBase):
    """Union base class"""
    ...
class Structure(_StructUnionBase):
    """Structure base class"""
    ...

class Array(_CData, Generic[_CT]):
    """
    Abstract base class for arrays.

    The recommended way to create concrete array types is by multiplying any
    ctypes data type with a non-negative integer. Alternatively, you can subclass
    this type and define _length_ and _type_ class variables. Array elements can
    be read and written using standard subscript and slice accesses for slice
    reads, the resulting object is not itself an Array.
    """
    @property
    @abstractmethod
    def _length_(self) -> int: ...
    @_length_.setter
    def _length_(self, value: int) -> None: ...
    @property
    @abstractmethod
    def _type_(self) -> type[_CT]: ...
    @_type_.setter
    def _type_(self, value: type[_CT]) -> None: ...
    # Note: only available if _CT == c_char
    @property
    def raw(self) -> bytes: ...
    @raw.setter
    def raw(self, value: ReadableBuffer) -> None: ...
    value: Any  # Note: bytes if _CT == c_char, str if _CT == c_wchar, unavailable otherwise
    # TODO These methods cannot be annotated correctly at the moment.
    # All of these "Any"s stand for the array's element type, but it's not possible to use _CT
    # here, because of a special feature of ctypes.
    # By default, when accessing an element of an Array[_CT], the returned object has type _CT.
    # However, when _CT is a "simple type" like c_int, ctypes automatically "unboxes" the object
    # and converts it to the corresponding Python primitive. For example, when accessing an element
    # of an Array[c_int], a Python int object is returned, not a c_int.
    # This behavior does *not* apply to subclasses of "simple types".
    # If MyInt is a subclass of c_int, then accessing an element of an Array[MyInt] returns
    # a MyInt, not an int.
    # This special behavior is not easy to model in a stub, so for now all places where
    # the array element type would belong are annotated with Any instead.
    def __init__(self, *args: Any) -> None: ...
    @overload
    def __getitem__(self, key: int, /) -> Any:
        """Return self[key]."""
        ...
    @overload
    def __getitem__(self, key: slice, /) -> list[Any]:
        """Return self[key]."""
        ...
    @overload
    def __setitem__(self, key: int, value: Any, /) -> None:
        """Set self[key] to value."""
        ...
    @overload
    def __setitem__(self, key: slice, value: Iterable[Any], /) -> None:
        """Set self[key] to value."""
        ...
    def __iter__(self) -> Iterator[Any]: ...
    # Can't inherit from Sized because the metaclass conflict between
    # Sized and _CData prevents using _CDataMeta.
    def __len__(self) -> int:
        """Return len(self)."""
        ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any, /) -> GenericAlias:
            """See PEP 585"""
            ...

def addressof(obj: _CData, /) -> int:
    """
    addressof(C instance) -> integer
    Return the address of the C instance internal buffer
    """
    ...
def alignment(obj_or_type: _CData | type[_CData], /) -> int:
    """
    alignment(C type) -> integer
    alignment(C instance) -> integer
    Return the alignment requirements of a C instance
    """
    ...
def get_errno() -> int: ...
def resize(obj: _CData, size: int, /) -> None:
    """Resize the memory buffer of a ctypes instance"""
    ...
def set_errno(value: int, /) -> int: ...
def sizeof(obj_or_type: _CData | type[_CData], /) -> int:
    """
    sizeof(C type) -> integer
    sizeof(C instance) -> integer
    Return the size in bytes of a C instance
    """
    ...
