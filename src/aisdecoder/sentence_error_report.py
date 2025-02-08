
from dataclasses import dataclass
import json
from collections import defaultdict
from functools import cache 

from typing import TYPE_CHECKING, Union, Any
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
    _ais_msg_ids : dict[int,int] = defaultdict(int)

    def sentence_error_percentage(self) -> float:
        return self.total_errors() / self.text_lines
    
    def sentence_specific_error_percentage(self) -> dict[str, float]:
        tot_err = self.total_errors()
        return {
            "percentage_of_sentences_with_missing_time": self.missing_time / tot_err,
            "percentage_of_sentences_malformed": self.malformed / tot_err,
            "percentage_of_sentences_with_bad_data": self.bad_data / tot_err,
            "percentage_of_sentences_with_bad_checksum": self.bad_checksum / tot_err,
            "percentage_of_sentences_out_of_order": self.out_of_order / tot_err
        }
    
    def add_text_line(self) -> None:
        self.text_lines += 1

    def add_sentence(self) -> None:
        self.sentences_number += 1

    def add_ais_message_by_id(self, msg_id:int) -> None:
        self._ais_msg_ids[msg_id] += 1

    def from_exception(self, error_name) -> None:
        val = getattr(self, error_name)
        setattr(self, error_name, val+1)

    def total_errors(self) -> int:
        return self.empty + self.malformed + self.missing_time + self.bad_data + self.bad_checksum + self.out_of_order

    def _invariant(self) -> bool:
        return self.text_lines - self.sentences_number == self.total_errors()

    @cache
    def total_ais_messages(self) -> int:
        return sum(v for v in self._ais_msg_ids.values())

    def report(self) -> dict[str, Any]:
        sentence_stats = {
            "number_of_text_lines": self.text_lines,
            "number_of_empty_lines": self.empty,
            "number_of_total_errors": self.total_errors(),
            "number_of_valid_sentences": self.sentences_number,
            "number_of_ais_messages": self.total_ais_messages(),
            "sentences_error_invariant_coherence": self._invariant(),
            "percentage_of_sentences_with_error": self.sentence_error_percentage()
        }   

        sentence_stats = {
            **sentence_stats,
            **self.sentence_specific_error_percentage()
        }   

        def calc_perc(m):
            return (m/self.total_ais_messages())*100
                
        sentence_stats = {
            **{"number_of_ais_messages_of_type_"+ str(k): self._ais_msg_ids[k] for k in sorted(self._ais_msg_ids)},
            **{"percentage_of_ais_messages_of_type_" + str(k): calc_perc(self._ais_msg_ids[k])  for k in sorted(self._ais_msg_ids)},
            **sentence_stats
        }
        return sentence_stats
    
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



