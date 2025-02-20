


message_1_1 = {
    "raw": "!AIVDM,1,1,,A,13cm=`00000`iAnIJ3W;Ic220@0a,0*36,1738369261",
    "parsed": 
    {"id": 1, "repeat_indicator": 0, "mmsi": 247287200, "nav_status": 0, "rot_over_range": False, "rot": 0.0, 
     "sog": 0.0, "position_accuracy": 0, "x": 8.906338333333334, "y": 44.40218, 
     "cog": 291.79998779296875, "true_heading": 353, "timestamp": 1, "special_manoeuvre": 0, "spare": 0, "raim": False, "sync_state": 0, "slot_timeout": 4, "slot_number": 41}
}


message_3_1 = {
    "raw" : "!AIVDM,1,1,,A,33lltP0P@1Pe0H8I>o`f46mj21wh,0*61,1738369257",
    "parsed": {"id": 3, "repeat_indicator": 0, "mmsi": 256720000, "nav_status": 0, 
               "rot_over_range": True, "rot": -720.0032348632812, 
               "sog": 0.10000000149011612, "position_accuracy": 1, "x": 9.831686666666666,
                 "y": 44.096696666666666, "cog": 360.0, "true_heading": 218, "timestamp": 57, "special_manoeuvre": 0, "spare": 0, "raim": True, "sync_state": 0, "slot_increment": 511, "slots_to_allocate": 0, "keep_flag": False}
}

#has cog not valid (=360.0)
message_1_2 = {
    "raw": "!AIVDM,1,1,,A,13cuES?P00Pe;lLI>V2N4?wd28Og,0*02,1738369257",
    "parsed": {'id': 1, 'repeat_indicator': 0, 'mmsi': 247420300, 'nav_status': 15, 'rot_over_range': True, 'rot': -731.386474609375, 'sog': 0.0, 'position_accuracy': 1, 'x': 9.870743333333333, 'y': 44.08918833333333, 'cog': 360.0, 'true_heading': 511, 'timestamp': 54, 'special_manoeuvre': 0, 'spare': 0, 'raim': True, 'sync_state': 0, 'slot_timeout': 2, 'slot_number': 2031}
}

#invalid sog
message_3_2 ={
    "raw": "!AIVDM,1,1,,B,34h?wK50ww0g8vTHrWUf48ML0DwJ,0*1B",
    "parsed": {'id': 3, 'repeat_indicator': 0, 'mmsi': 319029100, 'nav_status': 5, 'rot_over_range': False, 'rot': 0.40176260471343994, 'sog': 102.30000305175781, 'position_accuracy': 0, 'x': 10.29795, 'y': 43.54371666666667, 'cog': 360.0, 'true_heading': 270, 'timestamp': 46, 'special_manoeuvre': 0, 'spare': 0, 'raim': False, 'sync_state': 0, 'slot_increment': 5373, 'slots_to_allocate': 5, 'keep_flag': False}
}


