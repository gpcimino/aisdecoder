from datetime import datetime

import ais  # type: ignore

from aisdecoder.exceptions import CannotDecodeVDMPaylaodError
from aisdecoder.ais_message import AISMessage
from aisdecoder.basictypes.mmsi import MMSI


from typing import Optional

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
            decoded_msg['name'],
            decoded_msg['imo_num']
        )

    def __init__(self, 
        time: datetime, 
        mmsi:MMSI, 
        reciver_class:str, 
        name: str,
        imo: int
    ):
        super().__init__(
            time, 
            mmsi, 
            reciver_class, 
        )
        self._name = name
        self._imo = imo

    def message_id(self) -> int:
        return 5

    def name(self) -> Optional[str]:
        if self._name is None:
            return None 
        return self._name.rstrip("@").strip()
    
    def imo(self) -> int:
        return self._imo

    def is_kinematic(self) -> bool:
        return False
    
    def has_valid_position(self) -> bool:
        return False

    def write(self, writer) -> None:
        writer.write_message5(self)    