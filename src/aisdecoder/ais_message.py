from datetime import datetime
from abc import abstractmethod

from aisdecoder.message_errors import MessageErrors as Err
from aisdecoder.basictypes.mmsi import MMSI

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from datetime import timedelta


class AISMessage:
    def __init__(self, time: datetime, mmsi:MMSI, reciver_class:str) -> None:
        self._time : datetime = time
        self._mmsi : MMSI = mmsi
        self._receiver_class : str = reciver_class

    def message_id(self) -> int:
        raise NotImplementedError()

    def time(self) -> datetime:
        return self._time
    
    def MMSI(self) -> MMSI:
        return self._mmsi
    
    def validate_mmsi(self) -> Err:
        return self._mmsi.validate()
    
    def flag(self) -> Optional[str]:
        return self._mmsi.flag()
    
    def flag_short_name(self) -> Optional[str]:
        return self._mmsi.flag_short_name()
    
    def receiver_class(self) -> str:
        return self._receiver_class
    
    def receiver_class_validation(self) -> Err:
        if self._receiver_class in ["A", "B"]:
            return Err.OK
        else:
            return Err.BAD_RECEIVER_CLASS

    def is_kinematic(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def write(self, writer):
        raise NotImplementedError()
    
    def ellapsed_time(self, other: "AISMessage") -> "timedelta":
        return self.time() - other.time()
    
    def errors(self):
        return Err.OK
    
    def warnings(self):
        return Err.OK   

    # """
    # AIS Messages can contains wrong information.
    # AIS Message creation is lazy, that is object is created but no check is executed until fields are accessed
    # Here is how error are classified:

    # * Severe errors: AISParserError raise when field is accessed
    #     - bad latitude
    #     - bad longitude
    #     - time out of allowed range

    # * Errors: message object is created and errors field return a bit flag mask reporting the error type;
    # errors.is_any_set() return true. This happen for
    #     - bad MMSI, all flavor

    # * Warning:   message object is created and warnings() methods return a bit flag mask reporting the error type;
    # warnings.is_any_set() return True, errors.is_any_set() return False
    #     - SOG out of range value; note that is sog==3600 means not available and this is not a warning
    #     - ...
    # """

    # MIN_ALLOWED_TIME = 631152000  # 631152000 = 1990/1/1 00:00:00
    # MAX_ALLOWED_TIME = 4102444800  # 4102444800= 2100/1/1 00:00:00

    # def __init__(self, time: datetime, mmsi:int, reciver_class:str) -> None:
    #     self._time : datetime = time
    #     self._mmsi : int = mmsi
    #     self._receiver_class : str = reciver_class

    # def time(self) -> datetime:
    #     return self._time
    
    # def MMSI(self) -> int:
    #     return self._mmsi
    
    # def receiver_class(self) -> str:
    #     return self._receiver_class
    
    
    # def datetime(self, format_=None):
    #     t = time.gmtime(self.epoch_time())
    #     dt = datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    #     if format_ is None:
    #         return dt
    #     return dt.strftime(format_)

    # def MMSI(self):
    #     m = MMSI(self._msg_dict["mmsi"])
    #     m.validate()
    #     self.errors = self.errors.combine(m.errors)
    #     return m

    # def msg_id(self):
    #     id_ = self._msg_dict["id"]
    #     return id_

    # def receiver_class(self):
    #     return self._msg_dict["receiver_class"]

    # def nmea(self):
    #     if "nmea" not in self._msg_dict:
    #         raise AISParserError("AIS Message doesn't contain raw NMEA sentence")
    #     return self._msg_dict["nmea"]

    # def validate(self):
    #     try:
    #         self.epoch_time()
    #     except Exception: # pylint: disable=broad-except
    #         pass
    #     try:
    #         self.MMSI()
    #     except Exception: # pylint: disable=broad-except
    #         pass
    #     return self.errors

    # def qa(self):
    #     # use the most 8 significant bits for errors, the first 24 bits for warnings
    #     return self.errors.combine(self.warnings, shift=24)

    # def qa_as_int(self):
    #     return int(self.qa())

    # def qa_as_str(self):
    #     return self.qa().to_verbose_str()

    # def print(self, media):
    #     raise NotImplementedError()

    # def has_kinematic_info(self):
    #     raise NotImplementedError()

    # def has_static_info(self):
    #     raise NotImplementedError()

    # def has_native_static_info(self):
    #     raise NotImplementedError()

    # def add_static(self, msg_static):
    #     self._msg_dict["static"] = msg_static

    # def static_info(self):
    #     return self._msg_dict["static"]
