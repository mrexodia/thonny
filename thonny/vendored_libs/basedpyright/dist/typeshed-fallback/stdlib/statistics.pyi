import sys
from _typeshed import SupportsRichComparisonT
from collections.abc import Callable, Hashable, Iterable, Sequence
from decimal import Decimal
from fractions import Fraction
from typing import Any, Literal, NamedTuple, SupportsFloat, TypeVar
from typing_extensions import Self, TypeAlias

__all__ = [
    "StatisticsError",
    "fmean",
    "geometric_mean",
    "mean",
    "harmonic_mean",
    "pstdev",
    "pvariance",
    "stdev",
    "variance",
    "median",
    "median_low",
    "median_high",
    "median_grouped",
    "mode",
    "multimode",
    "NormalDist",
    "quantiles",
]

if sys.version_info >= (3, 10):
    __all__ += ["covariance", "correlation", "linear_regression"]
if sys.version_info >= (3, 13):
    __all__ += ["kde", "kde_random"]

# Most functions in this module accept homogeneous collections of one of these types
_Number: TypeAlias = float | Decimal | Fraction
_NumberT = TypeVar("_NumberT", float, Decimal, Fraction)

# Used in mode, multimode
_HashableT = TypeVar("_HashableT", bound=Hashable)

class StatisticsError(ValueError): ...

if sys.version_info >= (3, 11):
    def fmean(data: Iterable[SupportsFloat], weights: Iterable[SupportsFloat] | None = None) -> float: ...

else:
    def fmean(data: Iterable[SupportsFloat]) -> float: ...

def geometric_mean(data: Iterable[SupportsFloat]) -> float: ...
def mean(data: Iterable[_NumberT]) -> _NumberT: ...

if sys.version_info >= (3, 10):
    def harmonic_mean(data: Iterable[_NumberT], weights: Iterable[_Number] | None = None) -> _NumberT: ...

else:
    def harmonic_mean(data: Iterable[_NumberT]) -> _NumberT: ...

def median(data: Iterable[_NumberT]) -> _NumberT: ...
def median_low(data: Iterable[SupportsRichComparisonT]) -> SupportsRichComparisonT: ...
def median_high(data: Iterable[SupportsRichComparisonT]) -> SupportsRichComparisonT: ...

if sys.version_info >= (3, 11):
    def median_grouped(data: Iterable[SupportsFloat], interval: SupportsFloat = 1.0) -> float: ...

else:
    def median_grouped(data: Iterable[_NumberT], interval: _NumberT | float = 1) -> _NumberT | float: ...

def mode(data: Iterable[_HashableT]) -> _HashableT: ...
def multimode(data: Iterable[_HashableT]) -> list[_HashableT]: ...
def pstdev(data: Iterable[_NumberT], mu: _NumberT | None = None) -> _NumberT: ...
def pvariance(data: Iterable[_NumberT], mu: _NumberT | None = None) -> _NumberT: ...
def quantiles(
    data: Iterable[_NumberT], *, n: int = 4, method: Literal["inclusive", "exclusive"] = "exclusive"
) -> list[_NumberT]: ...
def stdev(data: Iterable[_NumberT], xbar: _NumberT | None = None) -> _NumberT: ...
def variance(data: Iterable[_NumberT], xbar: _NumberT | None = None) -> _NumberT: ...

class NormalDist:
    def __init__(self, mu: float = 0.0, sigma: float = 1.0) -> None: ...
    @property
    def mean(self) -> float:
        """Arithmetic mean of the normal distribution."""
        ...
    @property
    def median(self) -> float:
        """Return the median of the normal distribution"""
        ...
    @property
    def mode(self) -> float:
        """
        Return the mode of the normal distribution

        The mode is the value x where which the probability density
        function (pdf) takes its maximum value.
        """
        ...
    @property
    def stdev(self) -> float:
        """Standard deviation of the normal distribution."""
        ...
    @property
    def variance(self) -> float:
        """Square of the standard deviation."""
        ...
    @classmethod
    def from_samples(cls, data: Iterable[SupportsFloat]) -> Self: ...
    def samples(self, n: int, *, seed: Any | None = None) -> list[float]: ...
    def pdf(self, x: float) -> float: ...
    def cdf(self, x: float) -> float: ...
    def inv_cdf(self, p: float) -> float: ...
    def overlap(self, other: NormalDist) -> float: ...
    def quantiles(self, n: int = 4) -> list[float]: ...
    if sys.version_info >= (3, 9):
        def zscore(self, x: float) -> float: ...

    def __eq__(self, x2: object) -> bool: ...
    def __add__(self, x2: float | NormalDist) -> NormalDist: ...
    def __sub__(self, x2: float | NormalDist) -> NormalDist: ...
    def __mul__(self, x2: float) -> NormalDist: ...
    def __truediv__(self, x2: float) -> NormalDist: ...
    def __pos__(self) -> NormalDist: ...
    def __neg__(self) -> NormalDist: ...
    __radd__ = __add__
    def __rsub__(self, x2: float | NormalDist) -> NormalDist: ...
    __rmul__ = __mul__
    def __hash__(self) -> int: ...

if sys.version_info >= (3, 12):
    def correlation(
        x: Sequence[_Number], y: Sequence[_Number], /, *, method: Literal["linear", "ranked"] = "linear"
    ) -> float: ...

elif sys.version_info >= (3, 10):
    def correlation(x: Sequence[_Number], y: Sequence[_Number], /) -> float: ...

if sys.version_info >= (3, 10):
    def covariance(x: Sequence[_Number], y: Sequence[_Number], /) -> float: ...

    class LinearRegression(NamedTuple):
        slope: float
        intercept: float

if sys.version_info >= (3, 11):
    def linear_regression(
        regressor: Sequence[_Number], dependent_variable: Sequence[_Number], /, *, proportional: bool = False
    ) -> LinearRegression: ...

elif sys.version_info >= (3, 10):
    def linear_regression(regressor: Sequence[_Number], dependent_variable: Sequence[_Number], /) -> LinearRegression: ...

if sys.version_info >= (3, 13):
    _Kernel: TypeAlias = Literal[
        "normal",
        "gauss",
        "logistic",
        "sigmoid",
        "rectangular",
        "uniform",
        "triangular",
        "parabolic",
        "epanechnikov",
        "quartic",
        "biweight",
        "triweight",
        "cosine",
    ]
    def kde(
        data: Sequence[float], h: float, kernel: _Kernel = "normal", *, cumulative: bool = False
    ) -> Callable[[float], float]: ...
    def kde_random(
        data: Sequence[float],
        h: float,
        kernel: _Kernel = "normal",
        *,
        seed: int | float | str | bytes | bytearray | None = None,  # noqa: Y041
    ) -> Callable[[], float]: ...
