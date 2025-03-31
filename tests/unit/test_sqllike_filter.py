import unittest

from assertpy import assert_that

from aisdecoder.filters.sqllikefilter.sqllikefilter import SQLLikeFilter   
# from aisdecoder.basictypes.basic_types import Point
# from aisdecoder.message_errors import MessageErrors as err
from aisdecoder.create_message_helper import create_msg_123, create_msg_5

# from test_data import message_3_1, message_1_1, message_1_2, message_3_2, message_1_3

class TestAISKinematicMessage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_filter_by_one_kine_attribute_should_work(self):
        m = create_msg_123(sog=10.1)
        f = SQLLikeFilter(code="sog > 10")
        assert_that(f.match(m)).is_true()

    def test_filter_by_and_of_kine_attributes_should_work(self):
        m = create_msg_123(sog=10.1, cog=180)
        f = SQLLikeFilter(code="sog > 10 AND cog = 180")
        assert_that(f.match(m)).is_true()   

    def test_filter_enforcing_precedence_should_work(self):
        m = create_msg_123(sog=9.0, cog=180, true_heading=90)
        f = SQLLikeFilter(code="(sog > 10 AND cog = 180) OR true_heading=90")
        assert_that(f.match(m)).is_true()         

    def test_filter_by_name_should_work(self):
        m1 = create_msg_123()
        m5 = create_msg_5(vessel_name="ABC")
        m1.add_static(m5)
        f = SQLLikeFilter(code='name = "ABC"')
        assert_that(f.match(m1)).is_true()

    def test_filter_by_name_without_msg5_should_not_crash(self):
        m1 = create_msg_123()
        f = SQLLikeFilter(code='name = "ABC"')
        assert_that(f.match(m1)).is_false()  

    def test_filter_by_name_with_char_filler_should_work(self):
        m1 = create_msg_123()
        m5 = create_msg_5(vessel_name="ABC@@@@@@@@@")
        m1.add_static(m5)
        f = SQLLikeFilter(code='name = "ABC"')
        assert_that(f.match(m1)).is_true()       


    def test_filter_by_speed_and_name_should_work(self):
        m1 = create_msg_123(sog=5)
        m5 = create_msg_5(vessel_name="ABC")
        m1.add_static(m5)
        f = SQLLikeFilter(code='speed_over_ground > 4 AND name = "ABC" ')
        assert_that(f.match(m1)).is_true()          

        f = SQLLikeFilter(code='name = "ABC" AND speed_over_ground < 4')
        assert_that(f.match(m1)).is_false()                  