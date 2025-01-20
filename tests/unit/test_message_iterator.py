import unittest

from assertpy import assert_that

from aisdecoder.message_factory import AllMessagesFactory, KinematicMessagesFactory
from aisdecoder.vdm_sentence_structure import EndsWithEpochTime
from aisdecoder.message_iterator import MessageIterator

class TestMessageIterator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self._sentences = [
            "!AIVDM,2,1,9,A,53cegq82=vJDT9EN220Lu8Ltp62222222222221@5hM,0*0D,1632009604",
            "!AIVDM,2,2,9,A,2=4rTN<S2ESlSSp8888888888880,2*29,1632009604",
            "!AIVDM,1,1,,B,15Q?3T001WaD?dHCMNJJqHbt0>`<,0*45,1632009605"
        ]

    def test_parse_stream(self):

        builder = MessageIterator(
            self._sentences,
            sentence_structure = EndsWithEpochTime(),
            message_factory = AllMessagesFactory()
        )        
        messages = []
        for msg in builder:
            messages.append(msg)
        assert_that(messages).is_length(2)


    def test_parse_stream_with_garbage(self):
        self._sentences.insert(3, "jfkshfiw")
        self._sentences.append("!AIVDM,2,1,7,B,ENjOsqPsg@6a9Qh0W1WW0P000000NqSB<NkL000000N,0*6D")
        builder = MessageIterator(
            self._sentences,
            sentence_structure = EndsWithEpochTime(),
            message_factory = AllMessagesFactory()
        )        
        messages = []
        for msg in builder:
            messages.append(msg)
        assert_that(messages).is_length(2)

    def test_parse_stream_with_only_garbage(self):
        garbage = ["", "all your", "base", "are belong", None, "to us"]
        builder = MessageIterator(
            garbage,
            sentence_structure = EndsWithEpochTime(),
            message_factory = AllMessagesFactory()
        )        
        messages = []
        for msg in builder:
            messages.append(msg)
        assert_that(messages).is_length(0)        
    

    def test_parse_stream_skipp_unwanted_messages(self):
        builder = MessageIterator(
            self._sentences,
            sentence_structure = EndsWithEpochTime(),
            message_factory = KinematicMessagesFactory()
        )        
        messages = []
        for msg in builder:
            messages.append(msg)
        assert_that(messages).is_length(1)      