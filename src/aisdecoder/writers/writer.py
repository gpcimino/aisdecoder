from typing import TYPE_CHECKING, List, Optional
from abc import abstractmethod
if TYPE_CHECKING:
    from aisdecoder.ais_message import AISMessage
    from aisdecoder.ais_kinematic_message import AISKinematicMessage
    from aisdecoder.ais_message_123 import AISMessage123
    from aisdecoder.ais_message_5 import AISMessage5
    from aisdecoder.ais_message_18 import AISMessage18
    from aisdecoder.ais_message_19 import AISMessage19   
    from aisdecoder.filters.filter import Filter 

class Writer:
    def __init__(self, filters: Optional[List["Filter"]]):
        self._filters = filters if filters is not None else []

    def filters_match(self, message: "AISMessage") -> bool:
        return all([f.match(message) for f in self._filters])

    @abstractmethod
    def write_message123(self, message: "AISMessage123") -> None:
        pass
    
    @abstractmethod
    def write_message5(self, message: "AISMessage5") -> None:
        pass

    @abstractmethod
    def write_message18(self, message: "AISMessage18") -> None:
        pass

    @abstractmethod
    def write_message19(self, message: "AISMessage19") -> None:
        pass
