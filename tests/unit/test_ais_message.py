import unittest

from assertpy import assert_that

from aisdecoder.ais_message_123 import AISMessage123   
from aisdecoder.basictypes.basic_types import Point
from aisdecoder.message_errors import MessageErrors as err
from aisdecoder.create_message_helper import create_msg_123

class TestAISMessage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_validate_mmsi(self):
        m = create_msg_123(mmsi=123456789)
        assert_that(m.validate_mmsi()).is_not_equal_to(err.OK)

    def test_mmsi_should_return_flag_name(self):
        m = create_msg_123(mmsi=371752000)
        assert_that(m.flag()).is_equal_to("Panama")



 

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