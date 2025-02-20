from datetime import datetime

from aisdecoder.basictypes.basic_types import Point
from aisdecoder.ais_message_123 import AISMessage123
from aisdecoder.ais_message_5 import AISMessage5
from aisdecoder.basictypes.mmsi import MMSI


def create_msg_123(time=None, mmsi=None, receiver_class=None, longitude=None, latitude=None, cog=None, sog=None, 
                true_heading=None, position_accuracy=None, id=None, rot=None):
    
    return AISMessage123(
        time or datetime(2025, 1, 20, 22, 45, 1), 
        MMSI(mmsi) or MMSI(123456789),
        receiver_class or "A",
        Point(longitude or 9, latitude or 44),
        cog or 1800,
        sog or 9.5,
        true_heading or 180,
        position_accuracy or 1,
        id or 1,
        rot or 2.5
    )

def create_msg_5(time=None, mmsi=None, receiver_class=None, vessel_name=None):
    return AISMessage5(
        time or datetime(2025, 1, 20, 22, 45, 1), 
        mmsi or 123456789,
        receiver_class or "A",
        vessel_name or "Titanic"
    )