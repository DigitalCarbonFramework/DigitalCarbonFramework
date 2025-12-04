import typing

from pydantic import BaseModel


class Distribution(BaseModel):
    """Represent a distribution over multiple keys."""

    weights: dict[typing.Any, float]
    """Set of weights for different keys"""

    def model_post_init(self, __context) -> None:
        del __context
        if any(x < 0 for x in self.weights.values()):
            raise ValueError("Distribution expect only positive weights")
        self._total_weights = sum(self.weights.values())
        if self._total_weights == 0:
            raise ValueError("At least one weight must be non-null")

    @property
    def get_weight(self):
        return self.weights.get

    _Tget = typing.TypeVar("_Tget")

    def get_ratio(self, key, default: _Tget = None) -> float | _Tget:
        if self._total_weights == 0:
            return 0.0
        return (
            self.weights[key] / self._total_weights if key in self.weights else default
        )
