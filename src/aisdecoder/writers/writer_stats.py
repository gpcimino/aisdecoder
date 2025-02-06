import json
import math

from datetime import datetime, timedelta, timezone, timezone
from collections import defaultdict
from aisdecoder.message_errors import MessageErrors as Err
from aisdecoder.writers.writer import Writer
from aisdecoder.sentence_error_report import sentence_error_report_singleton

from typing import TYPE_CHECKING, List, Optional
if TYPE_CHECKING:
    from aisdecoder.ais_message import AISMessage
    from aisdecoder.ais_kinematic_message import AISKinematicMessage
    from aisdecoder.ais_message_123 import AISMessage123
    from aisdecoder.ais_message_5 import AISMessage5
    from aisdecoder.ais_message_18 import AISMessage18
    from aisdecoder.ais_message_19 import AISMessage19   
    from aisdecoder.filters.filter import Filter 
    from pathlib import Path

class WriterStats(Writer):
    def __init__(self, filters: Optional[List["Filter"]]=None):
        super().__init__(filters)
        self.processing_start_time_utc: Optional[datetime] = None
        self.processing_end_time_utc: Optional[datetime] =  None
        self.data_min_time_utc: datetime = datetime.max.replace(tzinfo=timezone.utc)
        self.data_max_time_utc: datetime = datetime.min.replace(tzinfo=timezone.utc)
        self.number_of_ais_messages = 0
        self._number_of_ais_messages_for_class: dict[str,int] = defaultdict(int)
        self._number_of_ais_messages_for_type: dict[int,int] = defaultdict(int)
        # self.ais_messages_with_bad_mmsi: int = 0
        # self.ais_messages_with_bad_latitude: int = 0
        # self.ais_messages_with_bad_longitude: int = 0   
        self.ais_messages_warnings: dict[str,int] = defaultdict(int)
        self.ais_messages_errors: dict[str,int] = defaultdict(int)

    def processing_duration(self) -> timedelta:
        if self.processing_end_time_utc is not None and self.processing_start_time_utc is not None:
            return self.processing_end_time_utc - self.processing_start_time_utc
        raise ValueError("Cannot calculate processing duration with null start/end processing time")

    def write_message(self, message: "AISMessage") -> None:
        self._set_processing_start_time()
        self.number_of_ais_messages +=1
        self._number_of_ais_messages_for_class[message.receiver_class()] += 1
        self._number_of_ais_messages_for_type[message.message_id()] += 1
        self.data_min_time_utc = min(self.data_min_time_utc, message.time())
        self.data_max_time_utc = max(self.data_max_time_utc, message.time())
        for e in message.errors():
            self.ais_messages_errors[repr(e)] +=1
        for w in message.warnings():
            self.ais_messages_warnings[repr(w)] += 1

    def write_message123(self, message: "AISMessage123") -> None:
        self.write_message(message)
    
    def write_message5(self, message: "AISMessage5") -> None:
        self.write_message(message)

    def write_message18(self, message: "AISMessage18") -> None:
        self.write_message(message)

    def write_message19(self, message: "AISMessage19") -> None:
        self.write_message(message)

    def _set_processing_start_time(self) -> None:
        if self.processing_start_time_utc is None:
            self.processing_start_time_utc = datetime.now(timezone.utc)
 
    def _set_processing_end_time(self) -> None:
        if self.processing_end_time_utc is None:
            self.processing_end_time_utc = datetime.now(timezone.utc)

    def _message_type_invariant_coherence(self) -> bool:
        return sum([n for n in self._number_of_ais_messages_for_type.values()]) == self.number_of_ais_messages
 
    def _messsage_class_invariant_coherence(self) -> bool:
        return sum([n for n in self._number_of_ais_messages_for_class.values()]) == self.number_of_ais_messages
    
    def report(self) -> dict[str, int | timedelta |  bool | float | None]:
        self._set_processing_end_time()
        stats = {
            "data_min_time_utc": self.data_min_time_utc.isoformat() if self.data_min_time_utc is not None else None,
            "data_max_time_utc": self.data_max_time_utc.isoformat() if self.data_max_time_utc is not None else None,
            "processing_start_time_utc": self.processing_start_time_utc.isoformat() if self.processing_start_time_utc is not None else None,
            "processing_end_time_utc": self.processing_end_time_utc.isoformat() if self.processing_end_time_utc is not None else None, 
            "processing_duration_seconds": self.processing_duration().total_seconds(),
            "number_of_ais_messages": self.number_of_ais_messages,
            "message_type_invariant_coherence": self._message_type_invariant_coherence(),
            "messsage_class_invariant_coherence": self._messsage_class_invariant_coherence(),
        }

        stats = {
            **{"number_of_ais_messages_class_"+ k.lower(): v for k, v in self._number_of_ais_messages_for_class.items()},
            **stats
        }
            
        stats={
            **{"number_of_ais_messages_for_type_"+ str(k): v for k, v in self._number_of_ais_messages_for_type.items()},
            **stats
        }

        stats={
            **sentence_error_report_singleton.report(),
            **stats
        }

        stats={
            **self.ais_messages_errors,
            **stats
        }
        stats={
            **self.ais_messages_warnings,
            **stats
        }



        return stats

    def save(self, file: "Path") -> None:
        with file.open("w") as f:   
            json.dump(self.report(), f)            