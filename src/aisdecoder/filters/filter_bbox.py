from abc import abstractmethod

from aisdecoder.filters.filter import Filter
from aisdecoder.ais_kinematic_message import AISKinematicMessage

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aisdecoder.ais_message import AISMessage

class FilterBBox(Filter):
    def __init__(self, bbox):
        self._bbox  =bbox

    def match(self, message: "AISMessage") -> bool:
        return isinstance(message, AISKinematicMessage) and self._bbox.contains(message.position())