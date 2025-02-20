from datetime import datetime

import ais  # type: ignore

from aisdecoder.ais_kinematic_message import AISKinematicMessage
from aisdecoder.exceptions import CannotDecodeVDMPaylaodError
from aisdecoder.basictypes.basic_types import Point
from aisdecoder.basictypes.mmsi import MMSI

from typing import TYPE_CHECKING, Any, Optional
if TYPE_CHECKING:
    from datetime import datetime
    from aisdecoder.ais_message_5 import AISMessage5



class AISMessage123(AISKinematicMessage):
    #first = False
    @classmethod
    def from_sentence(cls, sentence_payload, padding, receiver_class, time=None):
        try:
            decoded_msg = ais.decode(sentence_payload, padding)
        except ais.DecodeError as ade:
            raise CannotDecodeVDMPaylaodError(sentence_payload) from ade
        
        # print(sentence_payload)
        # print(decoded_msg)
        # if not AISMessage123.first:
        #     print("raw", "mmsi,x,y,cog,sog,true_heading,position_accuracy,id,rot")
        #     AISMessage123.first = True    
        # whole ={
        #     **{"raw": sentence_payload},
        #     **decoded_msg
        # } 
        # print(",".join(
        #     [str(whole[k]) for k in 
        #      ["raw", "mmsi", "x", "y", "cog", "sog", "true_heading", "position_accuracy", "id", "rot"]
        #     ]
        # ))

        return cls(
            time, 
            decoded_msg['mmsi'],
            receiver_class,
            Point(decoded_msg['x'], decoded_msg['y']),
            decoded_msg['cog'],
            decoded_msg['sog'],
            decoded_msg['true_heading'],
            decoded_msg['position_accuracy'],
            decoded_msg['id'],
            decoded_msg['rot']
        )

    def __init__(self, 
        time: datetime, 
        mmsi:MMSI, 
        reciver_class:str, 
        position: Point,
        cog:float, 
        sog:float, 
        true_heading:int, 
        position_accuracy: int,
        id: int,
        rot: float
    ):
        super().__init__(
            time, 
            mmsi, 
            reciver_class, 
            position, 
            cog, 
            sog, 
            true_heading, 
            position_accuracy
        )
        self._id = id
        self._rot: float = rot
        self.static_msg: Optional["AISMessage5"] = None

    def message_id(self) -> int:
        return self._id

    def rate_of_turn(self) -> float:
        return self._rot    
        
    def has_valid_rate_of_turn(self) -> bool:
        """Turn rate is encoded as follows:
        0 = not turning

        1…126 = turning right at up to 708 degrees per minute or higher

        1…-126 = turning left at up to 708 degrees per minute or higher

        127 = turning right at more than 5deg/30s (No TI available)

        -127 = turning left at more than 5deg/30s (No TI available)

        128 (80 hex) indicates no turn information available (default)

        Values between 0 and 708 degrees/min coded by ROTAIS=4.733 * SQRT(ROTsensor) degrees/min where ROTsensor is
        the Rate of Turn as input by an external Rate of Turn Indicator. ROTAIS is rounded to the nearest integer value.
        Thus, to decode the field value, divide by 4.733 and then square it. Sign of the field value should be preserved when squaring it, otherwise the left/right indication will be lost.
        128 ==> 731.3864840545559677391778660594
        """
        # if -720.0032348632812 <= self._rot <= 720.0032348632812:
        #     return True
        # if math.isclose(rot, 731.3864840545559677391778660594, rel_tol=1e-4):
        #     return None        
        return True


    def write(self, writer):
        writer.write_message123(self)

    def add_static(self, static_msg: "AISMessage5") -> None:
        self.static_msg = static_msg



# import logging
# import math

# from aisparser.ais_kinematic_message import AISKinematicMessage
# from aisparser.errors import AISParserFatalError
# from aisparser.errors import Warnings

# log = logging.getLogger(__name__)


# class AISMessage123(AISKinematicMessage):
#     def __init__(self, msg_dict):
#         super().__init__(msg_dict)
#         if not self.msg_id() in (1, 2, 3):
#             raise AISParserFatalError(f"AIS Message 123 created with wrong id {self.msg_id()}")

#     def rot(self):
#         """Turn rate is encoded as follows:
#         0 = not turning

#         1…126 = turning right at up to 708 degrees per minute or higher

#         1…-126 = turning left at up to 708 degrees per minute or higher

#         127 = turning right at more than 5deg/30s (No TI available)

#         -127 = turning left at more than 5deg/30s (No TI available)

#         128 (80 hex) indicates no turn information available (default)

#         Values between 0 and 708 degrees/min coded by ROTAIS=4.733 * SQRT(ROTsensor) degrees/min where ROTsensor is
#         the Rate of Turn as input by an external Rate of Turn Indicator. ROTAIS is rounded to the nearest integer value.
#         Thus, to decode the field value, divide by 4.733 and then square it. Sign of the field value should be preserved when squaring it, otherwise the left/right indication will be lost.
#         128 ==> 731.3864840545559677391778660594
#         """
#         rot = self._msg_dict["rot"]
#         if -720.0032348632812 <= rot <= 720.0032348632812:
#             return rot
#         if math.isclose(rot, 731.3864840545559677391778660594, rel_tol=1e-4):
#             return None
#         self.warnings.set_flag(Warnings.ROT_VALUE_OUT_OF_RANGE)
#         log.info("Bad rot value %s", rot)
#         return None

#     def navigational_status(self):
#         """see table on specs: http://catb.org/gpsd/AIVDM.html Table 7. Navigation Status"""
#         nav_stat = self._msg_dict["nav_status"]
#         if 0 <= nav_stat <= 14:
#             return nav_stat
#         if nav_stat == 15:
#             return None
#         log.info("Bad navigational status value %s", nav_stat)
#         return None

#     def has_kinematic_info(self):
#         return True

#     def has_static_info(self):
#         return "static" in self._msg_dict

#     def has_native_static_info(self):
#         return False

#     def coherent_static_msg_id(self, static_msg_id):
#         return static_msg_id == 5

#     def static(self):
#         return self._msg_dict.get("static", None)

#     def write(self, media):
#         media.write123(self)

#     def static_time(self):
#         if self.has_static_info():
#             return self._msg_dict["static"].epoch_time()
#         return None

#     def ship_type_id(self):
#         if self.has_static_info():
#             return self._msg_dict["static"].ship_type_id()
#         return None

#     def validate(self):
#         super().validate()
#         self.rot()
#         self.navigational_status()
