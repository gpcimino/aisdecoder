import json
import math

from datetime import datetime, timedelta, timezone, timezone
from collections import defaultdict, OrderedDict
from aisdecoder.message_errors import MessageErrors as Err
from aisdecoder.writers.writer import Writer
from aisdecoder.sentence_error_report import sentence_error_report_singleton

from typing import TYPE_CHECKING, List, Optional, Any
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
    def __init__(self, input_file: Optional["Path"]=None, filters: Optional[List["Filter"]]=None,calc_percentage: bool=True):
        super().__init__(filters)
        self._calc_percentage: bool = calc_percentage
        self._input_file = input_file
        self.processing_start_time_utc: Optional[datetime] = None
        self.processing_end_time_utc: Optional[datetime] =  None
        self.data_min_time_utc: datetime = datetime.max.replace(tzinfo=timezone.utc)
        self.data_max_time_utc: datetime = datetime.min.replace(tzinfo=timezone.utc)
        self.number_of_ais_messages = 0
        self._number_of_ais_messages_for_class: dict[str, int] = defaultdict(int)
        self._number_of_ais_messages_for_type: dict[int, int] = defaultdict(int)
        self.ais_messages_warnings: dict[str, int] = defaultdict(int)
        self.ais_messages_errors: dict[str, int] = defaultdict(int)

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
            self.ais_messages_errors["number_of_parsed_ais_messages_with_" + repr(e)] +=1
        for w in message.warnings():
            self.ais_messages_warnings["number_of_parsed_ais_messages_with_" +repr(w)] += 1

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

    def calc_perc(self, m):
        return (m / self.number_of_ais_messages)*100

    def messages_per_class(self) -> OrderedDict[str, int | float]:
        msgs: OrderedDict[str, int | float] = OrderedDict({
            "number_of_parsed_ais_messages_of_class_"+ k.lower(): v 
            for k, v 
            in self._number_of_ais_messages_for_class.items()
        })
        if self._calc_percentage:
           msgs = OrderedDict({
            **msgs,
            **OrderedDict({
                "percentage_of_parsed_ais_messages_of_class_"+ k.lower(): self.calc_perc(v) 
                for k, v 
                in self._number_of_ais_messages_for_class.items()
            }),
        })
        return msgs
    
    def messages_per_type(self) -> OrderedDict[str, int | float]:
        msgs: OrderedDict[str, int | float] = OrderedDict({
            "number_of_parsed_ais_messages_of_type_"+ str(k): v 
            for k, v 
            in self._number_of_ais_messages_for_type.items()
        })
        if self._calc_percentage:
            msgs = OrderedDict({
                **msgs,
                **OrderedDict({
                    "percentage_of_parsed_ais_messages_of_type_"+ str(k): self.calc_perc(v) 
                    for k, v 
                    in self._number_of_ais_messages_for_type.items()}),
            })
        return msgs
    
    def messages_per_error(self) -> OrderedDict[str, int | float]:
        if self._calc_percentage:
            return OrderedDict({
                **self.ais_messages_errors,
                **OrderedDict({
                    k.replace("number_of_parsed_ais_messages_with_", "percentage_of_parsed_ais_messages_with_"): 
                    self.calc_perc(v)  
                    for k, v 
                    in self.ais_messages_errors.items()
                })
            })
        return OrderedDict(self.ais_messages_errors)
    
        
    def messages_per_warning(self) -> OrderedDict[str, int | float]:
        if self._calc_percentage:
            return OrderedDict({
                **self.ais_messages_warnings,
                **OrderedDict({
                    k.replace("number_of_parsed_ais_messages_with_", "percentage_of_parsed_ais_messages_with_"): 
                    self.calc_perc(v) 
                    for k, v 
                    in self.ais_messages_warnings.items()
                })  

            })
        return OrderedDict(self.ais_messages_warnings)

    def report(self) -> OrderedDict[str, dict[str, Any]]:
        self._set_processing_end_time()
        processing_stats = OrderedDict({
            "input_file": str(self._input_file),
            "processing_start_time_utc": self.processing_start_time_utc.isoformat() if self.processing_start_time_utc is not None else None,
            "processing_end_time_utc": self.processing_end_time_utc.isoformat() if self.processing_end_time_utc is not None else None, 
            "processing_duration_seconds": self.processing_duration().total_seconds(),
        })
        
        msg_stats: OrderedDict[str, Any] = OrderedDict({
            "ais_messages_min_time_utc": self.data_min_time_utc.isoformat() if self.data_min_time_utc is not None else None,
            "ais_messages_max_time_utc": self.data_max_time_utc.isoformat() if self.data_max_time_utc is not None else None,            
            "number_of_parsed_ais_messages": self.number_of_ais_messages,
            "message_type_invariant_coherence": self._message_type_invariant_coherence(),
            "messsage_class_invariant_coherence": self._messsage_class_invariant_coherence(),
        })
        # not sure why mypy is complaining about the following lines
        msg_stats = {**msg_stats, **self.messages_per_class()}  # type: ignore
        msg_stats = {**msg_stats, **self.messages_per_type()} # type: ignore
        msg_stats = {**msg_stats, **self.ais_messages_warnings} # type: ignore
        msg_stats = {**msg_stats, **self.ais_messages_errors} # type: ignore

        return OrderedDict({
            "processing_stats": processing_stats,
            "senteces_stats": sentence_error_report_singleton.report(),
            "messages_stats": msg_stats
        })

    def save(self, file: "Path") -> None:
        with file.open("w", encoding="utf-8") as f:   
            json.dump(self.report(), f)            