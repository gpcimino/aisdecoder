from enum import Flag

class MessageErrors(Flag):
    OK = 0
    BAD_LATITUDE = 2
    BAD_LONGITUDE = 4

    BAD_COURSE_OVER_GROUND = 8
    #BAD_RECEIVER_CLASS = 2

    def __repr__(self):
        return self.name.lower()


