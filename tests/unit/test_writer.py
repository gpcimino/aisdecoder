import unittest
from datetime import datetime, timezone
from io import StringIO

from assertpy import assert_that

from aisdecoder.create_message_helper import create_msg_123
from aisdecoder.writers.writer_csv import WriterCSV
from aisdecoder.basictypes.basic_types import Point

class TestWriter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_x(self):
        csv = StringIO("")
        wr = WriterCSV(csv)
        wr.write_message123(
            create_msg_123(
                time=datetime(2025, 1, 1, 10, 20, 1, tzinfo=timezone.utc),
                mmsi=370394000, 
                receiver_class="A", 
                latitude=10.1, 
                longitude=14.2,
                cog=3.2, 
                sog=4.5, 
                true_heading=180, 
                position_accuracy=1,
                id=1,
                rot=4.1
            )
        )
        assert_that(csv.getvalue()).is_equal_to("1735726801,370394000,1,14.2,10.1,3.2,4.5,180,1,4.1,\n")

        