import ais  # type: ignore

from aisdecoder.ais_message_18 import AISMessage18
from aisdecoder.basictypes.mmsi import MMSI


from typing import Optional

class AISMessage19(AISMessage18):
    @classmethod
    def from_sentence(cls, sentence_payload, padding, receiver_class, time=None):
        try:

            decoded_msg = ais.decode(sentence_payload, padding)
        except ais.DecodeError as ade:
            return None
        decoded_msg['receiver_class'] = receiver_class
        decoded_msg['time']=time
        return cls(decoded_msg)

    def __init__(self, parsed_msg):
        for key, value in parsed_msg.items():
            setattr(self, key, value)
        self._name = None

    def message_id(self) -> int:
        return 19

    
    def name(self) -> Optional[str]:
        if self._name is None:
            return None 
        return self._name.rstrip("@").strip()

    
    def write(self, writer):
        self.write_message19(self)     