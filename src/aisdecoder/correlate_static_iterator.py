from datetime import timedelta

from aisdecoder.basictypes.mmsi import MMSI

from typing import TYPE_CHECKING, Dict, Optional, Iterator
if TYPE_CHECKING: 
    from aisdecoder.ais_message_123 import AISMessage123
    from aisdecoder.ais_message_5 import AISMessage5
    from aisdecoder.ais_message import AISMessage

class CorrelateStaticIterator:
    def __init__(self, message_iterator: Iterator["AISMessage"], valid_time: Optional[timedelta]=None):
        self._message_iterator: Iterator["AISMessage"] = iter(message_iterator)
        self._valid_time: Optional[timedelta] = valid_time
        self._cache: Dict[MMSI, "AISMessage5"] = {}

    def __iter__(self):
        return self  # An iterator must return itself
    
    def __next__(self):
        for msg in self._message_iterator:
            if msg.message_id() in [1,2,3]:
                static_msg = self._get_last_static_or_none(msg)
                if static_msg is not None:
                    msg.add_static(static_msg)
            elif msg.message_id() == 5:
                self._add_cache(msg)
            else:
                pass
            return msg
        raise StopIteration()
    
    def _get_last_static_or_none(self, msg: "AISMessage123") -> Optional["AISMessage5"]:
        match:  Optional["AISMessage5"] = self._cache.get(msg.MMSI(), None)
        if self._valid_time is None:
            return match
        if match and msg.ellapsed_time(match) <= self._valid_time:
            return match
        return None

    def _add_cache(self, msg: "AISMessage5") -> None:
        self._cache[msg.MMSI()] = msg