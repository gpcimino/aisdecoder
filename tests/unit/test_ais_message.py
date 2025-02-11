import unittest
from datetime import datetime   
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

    def test_correct_mmsi_should_validate(self):
        m = create_msg_123(mmsi=371752000)
        assert_that(m.validate_mmsi()).is_equal_to(err.OK)

    def test_short_mmsi_should_not_validate(self):
        m = create_msg_123(mmsi=71752000)
        assert_that(m.validate_mmsi()).is_equal_to(err.BAD_MMSI)

    def test_mmsi_with_char_should_not_validate(self):
        m = create_msg_123(mmsi="abc")
        assert_that(m.validate_mmsi()).is_equal_to(err.BAD_MMSI)

    def test_invalid_mid_should_not_validate(self):
        m = create_msg_123(mmsi="975123456")
        assert_that(m.validate_mmsi()).is_equal_to(err.BAD_MMSI)   

    def test_invalid_ship_mid_should_not_validate(self):
        m = create_msg_123(mmsi="299752000")
        assert_that(m.validate_mmsi()).is_equal_to(err.BAD_MMSI)

    def test_invalid_sar_mid_should_not_validate(self):
        m = create_msg_123(mmsi="111299123")
        assert_that(m.validate_mmsi()).is_equal_to(err.BAD_MMSI)        

    def test_correct_mmsi_should_return_country(self):
        m = create_msg_123(mmsi=371752000)
        assert_that(m.flag()).is_equal_to("Panama")

    def test_correct_mmsi_should_return_country(self):
        m = create_msg_123(mmsi=247752000)
        assert_that(m.flag_short_name()).is_equal_to("IT")

    def test_invalid_mid_should_return_none_flag(self):
        m = create_msg_123(mmsi="975123456")
        assert_that(m.flag()).is_none()
 
    def test_invalid_mid_should_return_none_flag_short_name(self):
        m = create_msg_123(mmsi="975123456")
        assert_that(m.flag_short_name()).is_none()

    def test_validate_reciever_class(self):
        m = create_msg_123(receiver_class="A")
        assert_that(m.receiver_class()).is_equal_to("A")
        assert_that(m.receiver_class_validation()).is_equal_to(err.OK)

    def test_validate_reciever_class(self):
        m = create_msg_123(receiver_class="Z")
        assert_that(m.receiver_class_validation()).is_equal_to(err.BAD_RECEIVER_CLASS)

    def test_time(self):
        t=datetime(2025, 1, 20, 22, 45, 1)
        m = create_msg_123(time=t)
        assert_that(m.time()).is_equal_to(t)

    # def test_validate_all_message(self):
    #     m = create_msg_123(receiver_class="Z", position=Point(181, 45))
    #     assert_that(m.validate()).is_equal_to(Error.BAD_LONGITUDE & Error.BAD_RECEIVER_CLASS)