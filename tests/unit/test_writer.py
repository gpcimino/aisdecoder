import unittest
from datetime import datetime, timezone
from io import StringIO

from assertpy import assert_that

from aisdecoder.ais_message_123 import AISMessage123
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
            AISMessage123(
                datetime(2025, 1, 1, 10, 20, 1, tzinfo=timezone.utc),
                370394000, 
                "A", 
                Point(10.1, 14.2),
                3.2, 
                4.5, 
                180, 
                1,
                1,
                4.1
            )
        )
        assert_that(csv.getvalue()).is_equal_to("1735726801,370394000,1,10.1,14.2,3.2,4.5,180,1,4.1,\n")

        