import unittest

from assertpy import assert_that

from aisdecoder.filters.sqllikefilter.sqllikefilter import SQLLikeFilter   
# from aisdecoder.basictypes.basic_types import Point
# from aisdecoder.message_errors import MessageErrors as err
from aisdecoder.create_message_helper import create_msg_123

# from test_data import message_3_1, message_1_1, message_1_2, message_3_2, message_1_3

class TestAISKinematicMessage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_filter_by_one_kine_attribute_should_work(self):
        m = create_msg_123(sog=10.1)
        f = SQLLikeFilter(code="_sog > 10")
        assert_that(f.match(m)).is_true()

    def test_filter_by_and_of_kine_attributes_should_work(self):
        m = create_msg_123(sog=10.1, cog=180)
        f = SQLLikeFilter(code="_sog > 10 AND _cog = 180")
        assert_that(f.match(m)).is_true()   

    def test_filter_enforcing_precedence_should_work(self):
        m = create_msg_123(sog=9.0, cog=180, true_heading=90)
        f = SQLLikeFilter(code="(_sog > 10 AND _cog = 180) OR _true_heading=90")
        assert_that(f.match(m)).is_true()               