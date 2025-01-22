from enum import Flag

class Error(Flag):
    OK = 0
    BAD_RECEIVER_CLASS = 2
    BAD_LONGITUDE = 4
    BAD_LATITUDE = 8

    MALFORMED_SENTENCE = 16


