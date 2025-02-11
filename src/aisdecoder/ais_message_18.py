from datetime import datetime

import ais  # type: ignore

from aisdecoder.ais_kinematic_message import AISKinematicMessage
from aisdecoder.exceptions import CannotDecodeVDMPaylaodError
from aisdecoder.basictypes.basic_types import Point
from aisdecoder.basictypes.mmsi import MMSI

class AISMessage18(AISKinematicMessage):
    @classmethod
    def from_sentence(cls, sentence_payload, padding, receiver_class, time=None):
        try:
            decoded_msg = ais.decode(sentence_payload, padding)
        except ais.DecodeError as ade:
            raise CannotDecodeVDMPaylaodError(sentence_payload) from ade
        #print(decoded_msg)
        return cls(
            time, 
            decoded_msg['mmsi'],
            receiver_class,
            Point(decoded_msg['x'], decoded_msg['y']),
            decoded_msg['cog'],
            decoded_msg['sog'],
            decoded_msg['true_heading'],
            decoded_msg['position_accuracy']
        )

    def __init__(self, 
        time: datetime, 
        mmsi:MMSI, 
        reciver_class:str, 
        position: Point,
        cog:float, 
        sog:float, 
        true_heading:int, 
        position_accuracy: int
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
        pass
    
    def message_id(self) -> int:
        return 18
        
    def write(self, writer):
        writer.write_message18(self)
