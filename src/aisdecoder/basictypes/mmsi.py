from aisdecoder.basictypes.mids import mids   

class MMSI:
    def __init__(self, value:str):
        self._value: str = str(value)

    def __str__(self):
        return str(self._value)
    
    def flag(self) -> int:
        mid = self._get_mid()
        if mid in mids:
            return mids[mid]["country"]
        else:
            return None
    
    def flag_short_name(self) -> int:
        mid = self._get_mid()
        return mids[mid]["abbreviation"]    
    
    def _get_mid(self):
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
            return mmsi_str[2:5]
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
            raise ValueError(f"Unknown MMSI type {self._value}")
        
        #     if not (200 <= mid_num <= 799):
        # return False, f"Invalid MID {mid}. Ship station MIDs must be between 200 and 799"
    