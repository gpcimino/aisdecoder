from datetime import datetime, timezone

from aisdecoder.exceptions import MissingTimeSentenceError


class SentenceStructure():
    pass

class EndsWithEpochTime(SentenceStructure):
    def time(self, sentence: str) -> datetime:
        try:
            epoch = int(sentence.rsplit(",", maxsplit=1)[-1])
            return datetime.fromtimestamp(epoch, timezone.utc)
        except TypeError: 
            raise MissingTimeSentenceError("Cannot find valid epoch time at the end of the sentence", sentence) 
        
    def nmea_vdm_payload(self, sentence: str) -> str:
        return sentence.rsplit(",", maxsplit=1)[0]

class RealTimeSentence(SentenceStructure):
    def time(self, sentence: str) -> datetime:
        return datetime.now(timezone.utc)
   
    def nmea_vdm_payload(self, sentence: str) -> str:
        return sentence
    
class FixTimeSentence(SentenceStructure):
    def __init__(self, fix_time: datetime):
        self._fix_time = fix_time

    def time(self, sentence: str) -> datetime:
        return self._fix_time
   
    def nmea_vdm_payload(self, sentence: str) -> str:
        return sentence    