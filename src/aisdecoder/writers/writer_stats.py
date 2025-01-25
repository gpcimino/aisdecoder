import json
from collections import defaultdict

from aisdecoder.message_errors import MessageErrors as Err
from aisdecoder.writers.writer import Writer

from typing import TYPE_CHECKING, List
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
    def __init__(self, filters: List["Filter"]=None):
        super().__init__(filters)
        self.errors = defaultdict(int)
        self.warnings = defaultdict(int)

    def write_message(self, message: "AISMessage") -> None:
        for e in message.errors():
            self.errors[repr(e)] +=1
        for w in message.warnings():
            self.warnings[repr(w)] += 1


    def write_message123(self, message: "AISMessage123") -> None:
        self.write_message(message)
    
    def write_message5(self, message: "AISMessage5") -> None:
        self.write_message(message)

    def write_message18(self, message: "AISMessage18") -> None:
        self.write_message(message)

    def write_message19(self, message: "AISMessage19") -> None:
        self.write_message(message)

    def report(self) -> dict[str, dict[str,int]]:
        return {
            "errors": self.errors,
            "warnings": self.warnings
        } 

    def save(self, file: "Path") -> None:
        with file.open("w") as f:   
            json.dump(self.report(), f)            