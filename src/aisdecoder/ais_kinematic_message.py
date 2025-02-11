import logging
from datetime import datetime

from aisdecoder.ais_message import AISMessage
from aisdecoder.basictypes.basic_types import Point
from aisdecoder.message_errors import MessageErrors as Err
from aisdecoder.basictypes.mmsi import MMSI

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from datetime import datetime

log = logging.getLogger(__name__)


class AISKinematicMessage(AISMessage):
    def __init__(self, 
        time: datetime, 
        mmsi:MMSI, 
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
    
    def position_uom(self) -> str:
        return "geographic coordinates"
    
    def validate_position(self)-> Err:
        err = Err.OK
        if not self._position.has_valid_latitude():
            err |= Err.BAD_LATITUDE
        if not self._position.has_valid_longitude():
            err |= Err.BAD_LONGITUDE
        return err
    
    def course_over_ground(self) -> Optional[float]:
        if self._cog == 3600:
            return None
        return self._cog
    
    def course_over_ground_uom(self) -> str:
        return "degrees, 0 is north"
    
    def validate_course_over_ground(self)-> Err:
        if not 0<= self._cog <= 3600:
            return Err.BAD_COURSE_OVER_GROUND
        return Err.OK    
    
    def speed_over_ground(self):
        return self._sog
    
    def true_heading(self):
        return self._true_heading
    
    def position_accuracy(self):
        return self._position_accuracy
    
    def is_inside(self, bbox):
        return bbox.contains(self._position)
    
    def errors(self):
        return self.validate_position() 
    
    def warnings(self):
        return self.validate_course_over_ground()

