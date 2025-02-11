from datetime import datetime, timedelta
import unittest

from assertpy import assert_that

from aisdecoder.correlate_static_iterator import CorrelateStaticIterator
from aisdecoder.create_message_helper import create_msg_123, create_msg_5
from aisdecoder.basictypes.mmsi import MMSI

class TestCorrelateStaticIterator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self._t0 = datetime(2025, 1, 20, 22, 45, 1)
        self._mmsi1 = MMSI(123456789)
        self._mmsi2 = MMSI(987654321)

    def test_msg5_after_msg1_should_correlate(self):

        iterator = CorrelateStaticIterator([
            create_msg_123(time=self._t0, mmsi=self._mmsi1),
            create_msg_5(time=self._t0 + timedelta(seconds=10), mmsi=self._mmsi1),
            create_msg_123(time=self._t0 + timedelta(seconds=20), mmsi=self._mmsi1),
        ])
        correlated_msgs = [m for m in iterator]
        assert_that(correlated_msgs).is_length(3)
        assert_that(correlated_msgs[0].static_msg).is_none()
        assert_that(correlated_msgs[2].static_msg).is_equal_to(correlated_msgs[1])

    def test_msg5_after_different_msg1_should_not_correlate(self):

        iterator = CorrelateStaticIterator([
            create_msg_123(time=self._t0, mmsi=self._mmsi1),
            create_msg_5(time=self._t0 + timedelta(seconds=10), mmsi=self._mmsi2),
            create_msg_123(time=self._t0 + timedelta(seconds=20), mmsi=self._mmsi1),
        ])
        correlated_msgs = [m for m in iterator]
        assert_that(correlated_msgs).is_length(3)
        assert_that(correlated_msgs[0].static_msg).is_none()
        assert_that(correlated_msgs[2].static_msg).is_none()

    def test_msg5_after_ellapsed_time_since_msg1_should_not_correlate(self):

        iterator = CorrelateStaticIterator([
                create_msg_123(time=self._t0, mmsi=self._mmsi1),
                create_msg_5(time=self._t0 + timedelta(seconds=10), mmsi=self._mmsi1),
                create_msg_123(time=self._t0 + timedelta(seconds=20), mmsi=self._mmsi1),
            ],
            valid_time=timedelta(seconds=5)
        )
        correlated_msgs = [m for m in iterator]
        assert_that(correlated_msgs).is_length(3)
        assert_that(correlated_msgs[0].static_msg).is_none()
        assert_that(correlated_msgs[2].static_msg).is_none()    