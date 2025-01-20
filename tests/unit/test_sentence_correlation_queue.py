import unittest
from datetime import datetime
from assertpy import assert_that

from aisdecoder.vdm_sentence import SingleLineVDMSentenceNoChekcsum, MultiLineVDMSentence
from aisdecoder.sentence_correlation_queue import SentenceCorrelationQueue

class TestSentenceCorrelationQueue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self._scq = SentenceCorrelationQueue()
        self._s1 = SingleLineVDMSentenceNoChekcsum.create_realtime_sentence("!AIVDM,1,1,,B,15Q?3T001WaD?dHCMNJJqHbt0>`<,0*45")
        self._s2_1 = SingleLineVDMSentenceNoChekcsum.create_realtime_sentence("!AIVDM,2,1,7,B,ENjOsqPsg@6a9Qh0W1WW0P000000NqSB<NkL000000N,0*6D")
        self._s2_2 = SingleLineVDMSentenceNoChekcsum.create_realtime_sentence("!AIVDM,2,2,7,B,010,4*27")

    def test_single_sentence_should_create_message(self):
        self._scq.push(self._s1)
        assert_that(self._scq.is_sentence_ready()).is_true()

    def test_partial_multipart_sentence_should_not_create_message(self):
        self._scq.push(self._s2_1)
        assert_that(self._scq.is_sentence_ready()).is_false()

    def test_partial_multipart_sentence_should_not_create_message_2(self):
        self._scq.push(self._s2_2)
        assert_that(self._scq.is_sentence_ready()).is_false()        

    def test_complete_multipart_sentence_should_create_message(self):
        self._scq.push(self._s2_1)
        self._scq.push(self._s2_2)        
        assert_that(self._scq.is_sentence_ready()).is_true()

    def test_complete_large_multipart_sentence_should_create_message(self):
        self._scq.push(SingleLineVDMSentenceNoChekcsum.create_realtime_sentence("!AIVDM,3,1,,B,15Q?3T001WaD?dHCMNJJqHbt0>`<,0*45"))
        self._scq.push(SingleLineVDMSentenceNoChekcsum.create_realtime_sentence("!AIVDM,3,2,7,B,ENjOsqPsg@6a9Qh0W1WW0P000000NqSB<NkL000000N,0*6D"))
        self._scq.push(SingleLineVDMSentenceNoChekcsum.create_realtime_sentence("!AIVDM,3,3,7,B,010,4*27"))
        assert_that(self._scq.is_sentence_ready()).is_true()

    def test_partial_multipart_sentence_should_not_create_message(self):
        self._scq.push(self._s2_1)
        assert_that(self._scq.is_sentence_ready()).is_false()

    def test_missing_central_sentence_should_not_create_message(self):
        self._scq.push(SingleLineVDMSentenceNoChekcsum.create_realtime_sentence("!AIVDM,3,1,,B,15Q?3T001WaD?dHCMNJJqHbt0>`<,0*45"))
        self._scq.push(SingleLineVDMSentenceNoChekcsum.create_realtime_sentence("!AIVDM,3,3,7,B,010,4*27"))
        assert_that(self._scq.is_sentence_ready()).is_false()

    def test_queue_should_be_cleaned_up(self):
        self._scq.push(self._s1)
        self._scq.sentence()
        self._scq.push(self._s1)
        assert_that(self._scq.is_sentence_ready()).is_true()  
        assert_that(self._scq.sentence()).is_equal_to(
            self._s1
        )

    def test_queue_should_be_cleaned_up_after_error(self):
        self._scq.push(self._s2_2)
        assert_that(self._scq.is_sentence_ready()).is_false()  
        assert_that(self._scq.sentence).raises(Exception).when_called_with()
        self._scq.push(self._s1)
        assert_that(self._scq.is_sentence_ready()).is_true()  
        assert_that(self._scq.sentence()).is_equal_to(
            self._s1
        )      