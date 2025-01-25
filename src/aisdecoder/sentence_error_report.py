
from dataclasses import dataclass
import json

from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from pathlib import Path  

Number = Union[int, float]


class SentenceErrorReport:
    text_lines: int = 0
    empty: int = 0
    missing_time: int = 0
    malformed: int = 0
    bad_data: int = 0
    bad_checksum: int = 0
    out_of_order: int = 0
    sentences_number: int = 0

    def _error_rate(self) -> float:
        return self.total_errors() / self.text_lines

    def add_text_line(self) -> None:
        self.text_lines += 1

    def add_sentence(self) -> None:
        self.sentences_number += 1

    def from_exception(self, error_name) -> None:
        val = getattr(self, error_name)
        setattr(self, error_name, val+1)

    def total_errors(self) -> int:
        return self.empty + self.malformed + self.missing_time + self.bad_data + self.bad_checksum + self.out_of_order

    def _invariant(self) -> bool:
        return self.text_lines - self.sentences_number == self.total_errors()


    def report(self) -> dict[str, Union[Number, dict[str,int]]]:
        return {
            "text_lines": self.text_lines,
            "total_errors": self.total_errors(),
            "sentences_number": self.sentences_number,
            "errors_breakdown": {
                "empty": self.empty,
                "malformed": self.malformed,
                "bad_data": self.bad_data,
                "bad_checksum": self.bad_checksum,
                "out_of_order": self.out_of_order,
            },
            "data_coherence": self._invariant(),
            "error_rate": self._error_rate()
        }    

    def save(self, file: "Path") -> None:
        with file.open("w") as f:   
            json.dump(self.report(), f) 

    def reset(self) -> None:
        self.text_lines = 0
        self.empty = 0
        self.missing_time = 0
        self.malformed = 0
        self.bad_data = 0
        self.bad_checksum = 0
        self.out_of_order = 0
        self.sentences_number = 0


sentence_error_report_singleton = SentenceErrorReport() 