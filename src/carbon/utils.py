import typing

from pydantic import BaseModel


class Distribution(BaseModel):
    """Represent a distribution over multiple keys."""

    weights: dict[typing.Any, float]
    """Set of weights for different keys"""

    def model_post_init(self, __context) -> None:
        del __context
        self._total_weights = sum(self.weights.values())

    @property
    def get_weight(self):
        return self.weights.get

    _Tget = typing.TypeVar("_Tget")

    def get_ratio(self, key, default: _Tget = None) -> float | _Tget:
        return (
            self.weights[key] / self._total_weights if key in self.weights else default
        )
