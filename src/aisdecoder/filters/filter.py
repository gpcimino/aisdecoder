from abc import abstractmethod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aisdecoder.ais_message import AISMessage

class Filter:
    @abstractmethod
    def match(self, message: "AISMessage") -> bool:
        pass