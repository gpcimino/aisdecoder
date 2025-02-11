from aisdecoder.basictypes.mids import mids   
from aisdecoder.message_errors import MessageErrors

from typing import Optional

class MMSI:
    def __init__(self, value:str) -> None:
        self._value: str = str(value)

    def __str__(self) -> str:
        return str(self._value)

    def validate(self) -> MessageErrors:
        if len(self._value) != 9:
            return MessageErrors.BAD_MMSI
        if not self._value.isdigit():
            return MessageErrors.BAD_MMSI
        mid = self._get_mid()   
        if mid is None:
            return MessageErrors.BAD_MMSI
        if mid not in mids:
            return MessageErrors.BAD_MMSI
        return MessageErrors.OK
    
    def flag(self) -> Optional[str]:
        mid = self._get_mid()
        if mid in mids:
            return mids[mid]["country"]
        else:
            return None
    
    def flag_short_name(self) -> Optional[str]:
        mid = self._get_mid()
        if mid in mids:
            return mids[mid]["abbreviation"]
        else:
            return None        

    def _get_mid(self) -> Optional[str]:
        if self._value[0] in "234567":
            # MIDXXXXXXX
            # Ship
            return self._value[:3]
        elif self._value[0] == "8":
            # 8MIDXXXXX
            # Diver’s radio (not used in the U.S. in 2013)
            return self._value[1:4]
        elif self._value[:2] == "00":
            # 00MIDXXXX
            # Coastal stations
            return self._value[2:5]
        elif self._value[0] == "0":
            # 0MIDXXXXX
            # Group of ships; the U.S. Coast Guard, for example, is 03699999
            return self._value[1:4]
        elif self._value[:3] == "111":
            # 111MIDXXX
            # SAR (Search and Rescue) aircraft
            return self._value[3:6]
        elif self._value[:2] == "99":
            # 99MIDXXXX
            # Aids to Navigation
            return self._value[2:5]
        elif self._value[:2] == "98":
            # 98MIDXXXX
            # Auxiliary craft associated with a parent ship
            return self._value[2:5]
        elif self._value[:3] == "970":
            # 970MIDXXX
            # AIS SART (Search and Rescue Transmitter)
            return self._value[3:6]
        elif self._value[:3] == "972":
            # 972XXXXXX
            # MOB (Man Overboard) device
            return self._value[3:6]
        elif self._value[:3] == "974":
            # 974XXXXXX
            # EPIRB (Emergency Position Indicating Radio Beacon) AIS
            return self._value[3:6]
        else:
            return None
       
        #     if not (200 <= mid_num <= 799):
        # return False, f"Invalid MID {mid}. Ship station MIDs must be between 200 and 799"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MMSI):
            return False
        return self._value == other._value
    
    def __hash__(self) -> int:
        return hash(self._value)