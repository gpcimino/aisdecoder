import logging
from datetime import datetime

from aisdecoder.ais_message import AISMessage
from aisdecoder.basictypes.basic_types import Point



from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datetime import datetime

log = logging.getLogger(__name__)


class AISKinematicMessage(AISMessage):
    def __init__(self, 
        time: datetime, 
        mmsi:int, 
        reciver_class:str, 
        position: Point,
        cog:float, 
        sog:float, 
        true_heading:int, 
        position_accuracy: int    
    ) -> None:
        super().__init__(time, mmsi, reciver_class)
        self._position: Point = position
        self._cog: float = cog
        self._sog: float = sog 
        self._true_heading: int = true_heading
        self._position_accuracy: int = position_accuracy

    def is_kinematic(self) -> bool:
        return True

    def position(self) -> Point:
        return self._position
    
    def has_valid_position(self)-> bool:
        return True
        #return Error.ok if in -90/90 -180/180 else retun error.bad_lat | error.bad_long
    
    def course_over_ground(self):
        return self._cog
    
    def speed_over_ground(self):
        return self._sog
    
    def true_heading(self):
        return self._true_heading
    
    def position_accuracy(self):
        return self._position_accuracy
    
    def is_inside(self, bbox):
        return bbox.contains(self._position)

