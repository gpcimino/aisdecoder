from datetime import datetime

import ais

from aisdecoder.exceptions import CannotDecodeVDMPaylaodError
from aisdecoder.ais_message import AISMessage

class AISMessage5(AISMessage):
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
            decoded_msg['name']
        )

    def __init__(self, 
        time: datetime, 
        mmsi:int, 
        reciver_class:str, 
        name: str
    ):
        super().__init__(
            time, 
            mmsi, 
            reciver_class, 
        )
        self._name = name

    def message_id(self) -> int:
        return 5

    def name(self) -> str:
        return self._name

    def is_kinematic(self) -> bool:
        return False
    
    def has_valid_position(self) -> bool:
        return False

    def write(self, writer) -> None:
        writer.write_message5(self)    