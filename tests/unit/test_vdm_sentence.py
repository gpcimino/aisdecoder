import unittest
from datetime import datetime, timezone

from assertpy import assert_that

from aisdecoder.message_factory import AllMessagesFactory
from aisdecoder.vdm_sentence_structure import FixTimeSentence
from aisdecoder.vdm_sentence import SingleLineVDMSentence, MultiLineVDMSentence
from aisdecoder.exceptions import MalformedSentenceError, BadChecksumSentenceError, EmptySentenceError


class TestVDMSentence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.s1 = "!AIVDM,1,1,,B,15Q?3T001WaD?dHCMNJJqHbt0>`<,0*45"
        self.s2 = "!AIVDM,2,1,3,A,53cp>=42E>ntT`q3:20<tiDl8T6222222222220l1P<,0*49"

        self.s3 = "!AIVDM,2,1,7,B,ENjOsqPsg@6a9Qh0W1WW0P000000NqSB<NkL000000N,0*6D"
        self.s4 = "!AIVDM,2,2,7,B,010,4*27"



    def test_null_sentence_should_raise(self):
        assert_that(SingleLineVDMSentence.create_realtime_sentence).raises(EmptySentenceError).when_called_with(None)

    def test_empty_sentence_should_raise(self):
        assert_that(SingleLineVDMSentence.create_realtime_sentence).raises(EmptySentenceError).when_called_with("")       

    def test_partial_checksum_should_raise(self):
        assert_that(SingleLineVDMSentence.create_realtime_sentence).raises(MalformedSentenceError).when_called_with("*45")  

    def test_garbage_should_raise(self):
        assert_that(SingleLineVDMSentence.create_realtime_sentence) \
            .raises(MalformedSentenceError) \
            .when_called_with("all your base are belong to us")

    def test_invalid_checksum_should_raise(self):
        assert_that(SingleLineVDMSentence.create_realtime_sentence) \
            .raises(BadChecksumSentenceError) \
            .when_called_with(self.s1.replace("*45","*40"))

    def test_broken_char_should_raise_due_invalid_checksum(self):
        assert_that(SingleLineVDMSentence.create_realtime_sentence) \
            .raises(BadChecksumSentenceError) \
            .when_called_with(self.s1.replace("?3T", "?XT"))

    def test_invalid_progress_number_should_raise_due_invalid_checksum(self):
        assert_that(SingleLineVDMSentence.create_realtime_sentence) \
            .raises(MalformedSentenceError) \
            .when_called_with(self.s1.replace(",1,1,", ",X,1,"))

    def test_single_sentence_should_not_be_multipart(self):
        s = SingleLineVDMSentence.create_realtime_sentence(self.s1)
        assert_that(s.is_multi_sentence()).is_false()


    def test_single_multipart_sentence_should_be_multipart(self):
        s = SingleLineVDMSentence.create_realtime_sentence(self.s2)
        assert_that(s.is_multi_sentence()).is_true()

    def test_single_multipart_sentence_should_not_have_complete_payload(self):
        s = SingleLineVDMSentence.create_realtime_sentence(self.s2)
        assert_that(s.is_payload_complete()).is_false()

    def test_single_part_sentence_should_have_complete_payload(self):
        s = SingleLineVDMSentence.create_realtime_sentence(self.s1)
        assert_that(s.is_payload_complete()).is_true()

    def test_source(self):         
        s = SingleLineVDMSentence.create_realtime_sentence(self.s1)
        assert_that(s.source()).is_equal_to("AI")   

    def test_sentence_type(self):         
        s = SingleLineVDMSentence.create_realtime_sentence(self.s1)
        assert_that(s.sentence_type()).is_equal_to("VDM")             

    def test_receiver_class(self):         
        s = SingleLineVDMSentence.create_realtime_sentence(self.s1)
        assert_that(s.receiver_class()).is_equal_to("B")

    def test_checksum_valid(self):
        s = SingleLineVDMSentence.create_realtime_sentence(self.s1)
        assert_that(s.verify_checksum()).is_true()

    def test_time(self):
        t = datetime(2024, 7, 7, 23, 59, 59)
        s = SingleLineVDMSentence(self.s1, FixTimeSentence(t), AllMessagesFactory())
        assert_that(s.time()).is_equal_to(t)

    def test_multiline_sentence_payload(self):
        s = MultiLineVDMSentence(
            [
                SingleLineVDMSentence.create_realtime_sentence(self.s3), 
                SingleLineVDMSentence.create_realtime_sentence(self.s4)
            ]
        )
        assert_that(s.payload()).is_equal_to("ENjOsqPsg@6a9Qh0W1WW0P000000NqSB<NkL000000N010")

    def test_multiline_sentence_checksum(self):
        s = MultiLineVDMSentence(
            [
                SingleLineVDMSentence.create_realtime_sentence(self.s3), 
                SingleLineVDMSentence.create_realtime_sentence(self.s4)
            ]
        )
        assert_that(s.verify_checksum()).is_true()


    # def test_create_message_123(self):
    #     s = VDMSentence("!AIVDM,1,1,,B,15Q?3T001WaD?dHCMNJJqHbt0>`<,0*45")
    #     self.assertEqual(s.create_message().id, 1)
    #     self.assertEqual(s.create_message().mmsi, 370394000)
    #     self.assertEqual(s.create_message().receiver_class, "B")
    #     #self.assertIsNone(s.create_message().time)

    # def test_create_message_5(self):
    #     s1 = VDMSentence("!AIVDM,2,1,9,A,53cegq82=vJDT9EN220Lu8Ltp62222222222221@5hM,0*0D")
    #     s2 = VDMSentence("!AIVDM,2,2,9,A,2=4rTN<S2ESlSSp8888888888880,2*29")
    #     s = CompositeVDMSentence([s1, s2])
    #     self.assertEqual(s.create_message().id, 5)
    #     self.assertEqual(s.create_message().mmsi, 247164900)
    #     self.assertEqual(s.create_message().receiver_class, "A")
    #     #self.assertIsNone(s.create_message().time)

    # def test_parse_epoch_time(self):
    #     s1 = VDMSentence("!AIVDM,1,1,,A,13c`s1`P00Pe0rPI?:200?wb2<1J,0*53,1632009601", EndsWithEpochTime())
    #     self.assertEqual(s1.time, datetime.fromtimestamp(1632009601, timezone.utc))

    # def test_chars_in_epoch_time_should_raise(self):
    #     with self.assertRaises(MalformedSenetence):
    #         s1 = VDMSentence("!AIVDM,1,1,,A,13c`s1`P00Pe0rPI?:200?wb2<1J,0*53,163200X601", EndsWithEpochTime())

    # def test_missing_epoch_time_should_raise(self):
    #     with self.assertRaises(MalformedSenetence):
    #         s1 = VDMSentence("!AIVDM,1,1,,A,13c`s1`P00Pe0rPI?:200?wb2<1J,0*53", EndsWithEpochTime())