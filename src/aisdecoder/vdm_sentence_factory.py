from collections.abc import Iterable

from aisdecoder.vdm_sentence_structure import SentenceStructure
from aisdecoder.vdm_sentence import SingleLineVDMSentence, MultiLineVDMSentence, SingleLineVDMSentenceNoChekcsum

class VDMSentenceFactory:
    def __init__(self, sentence_structure: SentenceStructure, message_factory, verify_checksum: bool = False) -> None:
        self._sentence_structure=sentence_structure
        self._message_factory = message_factory
        self._verify_chekcsum = verify_checksum
        
    def make_from_sequence(self, sentences):
        if not isinstance(sentences, Iterable):
            raise ValueError("Need an iterable of SingleLineVDMSentence to build a MultiLineVDMSentence")
        if len(sentences) == 1:
            return sentences[0]
        else:
            return MultiLineVDMSentence(sentences)
        
    def make_from_str(self, sentence: str):
        if self._verify_chekcsum:
            return SingleLineVDMSentence(sentence, self._sentence_structure, self._message_factory)  
        else:
            return SingleLineVDMSentenceNoChekcsum(sentence, self._sentence_structure, self._message_factory)