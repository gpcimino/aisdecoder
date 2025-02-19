from enum import Flag

class MessageErrors(Flag):
    OK = 0
    BAD_MMSI = 2
    BAD_LATITUDE = 4
    BAD_LONGITUDE = 8
    BAD_RECEIVER_CLASS = 16
    BAD_COURSE_OVER_GROUND = 32
    BAD_SPEED_OVER_GROUND = 64

    def __repr__(self):
        return self.name.lower()


