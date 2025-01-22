import unittest

from assertpy import assert_that

from aisdecoder.vdm_sentence import SingleLineVDMSentence
from aisdecoder.errors_report import error_report_singleton
from aisdecoder.extras.swallow_exceptions import ignored
from aisdecoder.error import Error



class TestErrrorhandling(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        error_report_singleton.reset()
        self.s1 = "!AIVDM,1,1,,B,15Q?3T001WaD?dHCMNJJqHbt0>`<,0*45"

        self.s2 = "!AIVDM,2,1,3,A,53cp>=42E>ntT`q3:20<tiDl8T6222222222220l1P<,0*49"

        self.s3 = "!AIVDM,2,1,7,B,ENjOsqPsg@6a9Qh0W1WW0P000000NqSB<NkL000000N,0*6D"
        self.s4 = "!AIVDM,2,2,7,B,010,4*27"

    def test_good_data_should_not_report_any_error(self):
        _ = SingleLineVDMSentence.create_realtime_sentence(self.s1)
        assert_that(error_report_singleton.has("sentences", "total_sentences")).is_equal_to(1)
        assert_that(error_report_singleton.has("sentences", "sentence_error")).is_equal_to(0)

    def test_malformed_sentence_should_report_an_error(self):
        with ignored(Exception):
            _ = SingleLineVDMSentence.create_realtime_sentence("!AIVDM,15Q?3T001WaD?dHCMNJJqHbt0>`<,0*45")
        assert_that(error_report_singleton.has("sentences", "total_sentences")).is_equal_to(0)
        assert_that(error_report_singleton.has("sentences", "MalformedSenetenceError")).is_equal_to(1)


    def test_malformed_sentence_and_bad_checksum_should_report_2_errors(self):
        with ignored(Exception):
            _ = SingleLineVDMSentence.create_realtime_sentence("!AIVDM,15Q?3T001WaD?dHCMNJJqHbt0>`<,0*45")
       
        _ = SingleLineVDMSentence.create_realtime_sentence(self.s1)
       
        with ignored(Exception):
          _ = SingleLineVDMSentence.create_realtime_sentence("!AIVDM,2,1,3,A,53cp>=42E>ntT`q3:20<tiDl8T6222222222220l1P<,0*99")

        assert_that(error_report_singleton.has("sentences", "total_sentences")).is_equal_to(1)
        assert_that(error_report_singleton.has("sentences", "MalformedSenetenceError")).is_equal_to(1)
        assert_that(error_report_singleton.has("sentences", "BadCheckSumError")).is_equal_to(1)           