from functools import reduce
from datetime import datetime, timezone
import re
from abc import ABC, abstractmethod

from aisdecoder.vdm_sentence_structure import RealTimeSentence
from aisdecoder.exceptions import MalformedSentenceError, BadChecksumSentenceError, BadDataSentenceError, MultiLineSentenceError, OuOfOrderSentenceError, EmptySentenceError
from aisdecoder.message_factory import AllMessagesFactory
from aisdecoder.sentence_error_report import sentence_error_report_singleton as err


from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from datetime import datetime

class VMDSentence(ABC):
    def __init__(self, message_factory) -> None:
        self._message_factory = message_factory

    @abstractmethod
    def msg_id(self) -> int:
        raise NotImplementedError()
    
    @abstractmethod
    def verify_checksum(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_payload_complete(self) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def is_multi_sentence(self) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def is_before(self, other) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def is_first(self) -> bool:
        raise NotImplementedError()
    
    @abstractmethod    
    def payload(self) -> str:
        raise NotImplementedError()
    
    @abstractmethod    
    def padding(self) -> int:
        raise NotImplementedError()
    
    @abstractmethod    
    def receiver_class(self) -> str:
        raise NotImplementedError()
    
    @abstractmethod    
    def time(self) -> datetime:
        raise NotImplementedError()
    
    def can_create_message(self) -> bool:
        return self._message_factory.can_create(self.msg_id())

    def create_message(self):
        return self._message_factory.make(
            self.msg_id(), 
            self.payload(), 
            self.padding(), 
            self.receiver_class(), 
            self.time()
        )
    

regex = re.compile(r"!([A-Z]{2})([A-Z]{3}),(\d),(\d),.*,([A-B]),(.+),(\d)\*([0-9a-fA-F]{2})")


class SingleLineVDMSentence(VMDSentence):
    @classmethod
    def create_realtime_sentence(cls, sentence_str: str) -> Any:
        return cls(sentence_str, RealTimeSentence(), AllMessagesFactory())
    
    def __init__(self, sentence_str: str, sentence_structure, message_factory):
        super().__init__(message_factory)
        err.add_text_line()
        if sentence_str is None or sentence_str == "":
            raise EmptySentenceError("Empty or null sentence")
     

        self._time = sentence_structure.time(sentence_str)
        self._nmea_vdm = sentence_structure.nmea_vdm_payload(sentence_str)

        match = regex.match(self._nmea_vdm)
        if not match:
            raise MalformedSentenceError("Bad VMD sentence structure", self._nmea_vdm)

        try:
            self._source = match.group(1)
            self._sentence_type = match.group(2)
            self._num_sent = int(match.group(3))
            self._prog_num = int(match.group(4))
            #self.unknown = tokens[3]
            self._receiver_class = match.group(5)
            self._payload = match.group(6)
            self._padding = int(match.group(7))
            self._checksum = int(match.group(8), 16)
        except ValueError as ver:
            raise BadDataSentenceError("Cannot parse/convert sentence data", sentence_str) from ver

        if not self.verify_checksum():
            raise BadChecksumSentenceError(sentence_str)

        #invariants:
        if self._prog_num > self._num_sent:
            raise OuOfOrderSentenceError(sentence_str)
        # if self._receiver_class not in ["A", "B"]:
        #     raise BadDataSentenceError("Wrong transmitter class " + self.receiver_class(), sentence_str)

        err.add_sentence()
        if self.is_payload_complete():
            err.add_ais_message_by_id(self.msg_id())
        #print(sentence_str)
            

    def msg_id(self):
        """Parse only the first char of the sentence to extarct only the AIS msg id (first 6 bits)"""
        v = ord(self._payload[0])
        v = v - 48
        if v > 40:
            v = v - 8
        return v

    def verify_checksum(self):
        return self._checksum == self._calc_checksum()

    def is_payload_complete(self):
        return self._num_sent == self._prog_num
    
    def is_multi_sentence(self):
        return self._num_sent > 1
    
    def is_before(self, other):
        if isinstance(other, SingleLineVDMSentence):  
            return self._prog_num+1 == other._prog_num
        return False
    
    def is_first(self):
        return self._prog_num == 1
    
    def payload(self):
        return self._payload
    
    def padding(self):
        return self._padding
    
    def receiver_class(self):
        return self._receiver_class
    
    def time(self):
        return self._time
    
    def source(self):
        return self._source
    
    def sentence_type(self):
        return self._sentence_type

    def __eq__(self, other):
        if isinstance(other, SingleLineVDMSentence):    
            return self._nmea_vdm == other._nmea_vdm
        return False
    
    def _calc_checksum(self):
        checksum =  reduce(lambda checksum, c: checksum ^ ord(c), self._nmea_vdm[1:-3], 0)
        return checksum    


class MultiLineVDMSentence(VMDSentence):
    def __init__(self, sentences) -> None:
        if (len(sentences)<2):
            raise MultiLineSentenceError("Cannot create multi-line sentence with less than 2 senetnces")
        super().__init__(sentences[0]._message_factory)
        self.sentences = sentences

    def msg_id(self):
        return self.sentences[0].msg_id()

    def verify_checksum(self):
        return all((s.verify_checksum() for s in self.sentences))

    def is_payload_complete(self):
        return self.sentences[-1].is_payload_complete()
    
    def is_multi_sentence(self):
        return True

    def is_before(self, other):
        raise NotImplemented()    

    def is_first(self):
        raise True
    
    def payload(self):
        return reduce(lambda whole_payload, sentence: whole_payload+sentence.payload(), self.sentences, "")
    
    def padding(self):
        return self.sentences[-1].padding()
    
    def receiver_class(self):
        return self.sentences[0].receiver_class()
    
    def time(self):
        return self.sentences[0].time()

    def __eq__(self, other):
        if isinstance(other, MultiLineVDMSentence):
            return all(x == y for x, y in zip(self.sentences, other.sentences))
        return False    


class SingleLineVDMSentenceNoChekcsum(SingleLineVDMSentence):
    def verify_checksum(self):
        return True