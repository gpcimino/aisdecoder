from pathlib import Path

from aisdecoder.writers.writer import Writer

from typing import TYPE_CHECKING, List, Optional
if TYPE_CHECKING:
    from aisdecoder.ais_message import AISMessage
    from aisdecoder.ais_kinematic_message import AISKinematicMessage
    from aisdecoder.ais_message_123 import AISMessage123
    from aisdecoder.ais_message_5 import AISMessage5
    from aisdecoder.ais_message_18 import AISMessage18
    from aisdecoder.ais_message_19 import AISMessage19   
    from aisdecoder.filters.filter import Filter 

class WriterCSV(Writer):
    def __init__(self, filepath_or_buffer: Path, filters: Optional[List["Filter"]]=None) -> None:
        super().__init__(filters)
        if isinstance(filepath_or_buffer, Path):
            self._fp = filepath_or_buffer.open("w")
        else:
            self._fp = filepath_or_buffer

    def _write_ais_message(self, message: "AISMessage") -> None:
        self._fp.write(
            f"{int(message.time().timestamp())},{message.MMSI()},{message.message_id()}"
        )

    def _write_kinematic_message(self, message: "AISKinematicMessage") -> None:   
        self._write_ais_message(message)        
        self._fp.write(
            f",{message.position().as_csv()},{message.course_over_ground()},{message.speed_over_ground()},{message.true_heading()},{message.position_accuracy()}"  
        )

    def write_message123(self, message: "AISMessage123") -> None:
        self._write_kinematic_message(message)
        self._fp.write(
            f",{message.rate_of_turn()},{message.static_msg.name() if message.static_msg is not None else ''}\n"
        )

    def write_message5(self, message: "AISMessage5") -> None:
        self._write_ais_message(message)       
        self._fp.write(
            f"{message.name()}\n"
        )

    def write_message18(self, message: "AISMessage18") -> None:
        self._write_kinematic_message(message)
        self._fp.write(
            f"\n"
        )        

    def write_message19(self, message: "AISMessage19") -> None:
        self._write_kinematic_message(message)      
        self._fp.write(
            f"\n"
        )    

 
    def close(self) -> None:
        if self._fp is not None:
            self._fp.close() 