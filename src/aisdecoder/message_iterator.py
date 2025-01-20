from aisdecoder.sentence_correlation_queue import SentenceCorrelationQueue
from aisdecoder.vdm_sentence import SingleLineVDMSentence
from aisdecoder.exceptions import SentenceError, MessageError


class MessageIterator:

    def __init__(self, sentence_str_iterator, sentence_structure, message_factory):
        self._sentence_str_iterator = iter(sentence_str_iterator)
        self._sentence_structure = sentence_structure
        self._message_factory = message_factory
        self._scq = SentenceCorrelationQueue()

    def __iter__(self):
        return self  # An iterator must return itself
    
    def __next__(self):
        has_msg = False
        msg=None
        while not has_msg:
            while not self._scq.is_sentence_ready():
                str_sentence  = next(self._sentence_str_iterator)
                try:
                    sentence = SingleLineVDMSentence(str_sentence, self._sentence_structure, self._message_factory)
                except SentenceError:
                    continue
                except ValueError:
                    continue
                self._scq.push(sentence)
            sentence = self._scq.sentence()
            has_msg = sentence.can_create_message()
            if not has_msg:
                continue
            try:
                msg = sentence.create_message()
            except MessageError:
                msg=None
                has_msg = False
        return msg

        