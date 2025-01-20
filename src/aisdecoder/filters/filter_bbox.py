from abc import abstractmethod

from aisdecoder.filters.filter import Filter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ais_message import AISMessage

class FilterBBox(Filter):
    def __init__(self, bbox):
        self._bbox  =bbox

    def match(self, message: "AISMessage") -> bool:
        return message.is_kinematic() and self._bbox.contains(message.position())