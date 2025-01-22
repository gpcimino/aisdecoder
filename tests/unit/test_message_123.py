import unittest

from assertpy import assert_that

from aisdecoder.create_message_helper import create_msg_123
from aisdecoder.basictypes.basic_types import Point
from enum import IntFlag, auto



from aisdecoder.error import Error

class TestMessage123(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    # def test_validate_reciever_class(self):
    #     m = create_msg_123(receiver_class="A")
    #     assert_that(m.receiver_class()).is_equal_to("A")
    #     #assert_that(m.receiver_class_validation()).is_equal_to(Error.OK)

    # def test_validate_reciever_class(self):
    #     m = create_msg_123(receiver_class="Z")
    #     assert_that(m.receiver_class_validation()).is_equal_to(Error.BAD_RECEIVER_CLASS)

    # def test_validate_all_message(self):
    #     m = create_msg_123(receiver_class="Z", position=Point(181, 45))
    #     assert_that(m.validate()).is_equal_to(Error.BAD_LONGITUDE & Error.BAD_RECEIVER_CLASS)