from typing import TYPE_CHECKING, Dict, Optional
if TYPE_CHECKING: 
    from aisdecoder.ais_message_123 import AISMessage123
    from aisdecoder.ais_message_5 import AISMessage5

class CorrelateStaticIterator:
    def __init__(self, message_iterator):
        self._message_iterator = iter(message_iterator)
        self._cache: Dict[int, "AISMessage5"] = {}

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
        return self._cache.get(msg.MMSI(), None)

    def _add_cache(self, msg: "AISMessage5") -> None:
        self._cache[msg.MMSI()] = msg