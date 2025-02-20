import unittest

from assertpy import assert_that

from aisdecoder.ais_message_123 import AISMessage123   
from aisdecoder.basictypes.basic_types import Point
from aisdecoder.message_errors import MessageErrors as err
from aisdecoder.create_message_helper import create_msg_123
from test_data import message_3_1, message_1_1, message_1_2, message_3_2

class TestAISKinematicMessage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_validate_correct_position(self):
        m = create_msg_123()
        assert_that(m.validate_position()).is_equal_to(err.OK)

    def test_validate_bad_latitude(self):
        m = create_msg_123(latitude=91)
        assert_that(m.validate_position()).is_equal_to(err.BAD_LATITUDE)        

    def test_validate_bad_longitude(self):
        m = create_msg_123(longitude=181)
        assert_that(m.validate_position()).is_equal_to(err.BAD_LONGITUDE)   

    def test_validate_bad_position(self):
        m = create_msg_123(latitude=91, longitude=181)
        assert_that(m.validate_position()).is_equal_to(err.BAD_LATITUDE | err.BAD_LONGITUDE)

    def test_correct_cog_should_validate(self):
        m = create_msg_123(cog=180)
        assert_that(m.course_over_ground()).is_equal_to(180.0)
        assert_that(m.validate_course_over_ground()).is_equal_to(err.OK)

    def test_cog_from_sentence_should_validate(self):
        m = AISMessage123.from_sentence(message_1_1["raw"].split(",")[5], 0, "A")
        assert_that(m.course_over_ground()).is_close_to(message_1_1['parsed']['cog'], 0.1)
        assert_that(m.validate_course_over_ground()).is_equal_to(err.OK)

    def test_invalid_cog_from_sentence_should_return_none(self):
        m = AISMessage123.from_sentence(message_1_2["raw"].split(",")[5], 0, "A")
        assert_that(m.course_over_ground()).is_none()
        assert_that(m.validate_course_over_ground()).is_equal_to(err.OK)

    def test_cog_360_should_return_none(self):
        m = create_msg_123(cog=360)
        assert_that(m.course_over_ground()).is_none()
        assert_that(m.validate_course_over_ground()).is_equal_to(err.OK)
 
    def test_invalid_cog_should_return_error(self):
        m = create_msg_123(cog=360.1)
        assert_that(m.course_over_ground()).is_not_none()
        assert_that(m.validate_course_over_ground()).is_equal_to(err.BAD_COURSE_OVER_GROUND)

    def test_correct_sog_should_validate(self):
        m = create_msg_123(sog=5.1)
        assert_that(m.speed_over_ground()).is_equal_to(5.1)
        assert_that(m.validate_speed_over_ground()).is_equal_to(err.OK)

    def test_sog_from_sentence_should_validate(self):
        m = AISMessage123.from_sentence(message_3_1["raw"].split(",")[5], 0, "A")
        assert_that(m.speed_over_ground()).is_close_to(message_3_1['parsed']['sog'], 0.1)
        assert_that(m.validate_speed_over_ground()).is_equal_to(err.OK)

    def test_invalid_sog_from_sentence_should_return_none(self):
        m = AISMessage123.from_sentence(message_3_2["raw"].split(",")[5], 0, "A")
        assert_that(m.speed_over_ground()).is_none()
        assert_that(m.validate_speed_over_ground()).is_equal_to(err.OK)
        
    def test_invalid_sog_should_return_error(self):
        m = create_msg_123(sog=-1)
        assert_that(m.speed_over_ground()).is_not_none()
        assert_that(m.validate_speed_over_ground()).is_equal_to(err.BAD_SPEED_OVER_GROUND)


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