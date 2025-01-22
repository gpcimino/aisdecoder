import re
from aisdecoder.sentence_error_report import sentence_error_report_singleton as err

pascal2snake_regex = re.compile('[A-Z]+[a-z]*')

def error_name(text):
  text = text.replace('SentenceError', '')
  tokens = re.findall(pascal2snake_regex, text)
  snake = '_'.join(tokens)
  return snake.lower()



class AISParserError(Exception):
    pass

class SentenceError(AISParserError):
    def __init__(self, err_msg, sentence_str):
        super().__init__(err_msg)
        self._senetence_str = sentence_str
        err.from_exception(error_name(self.__class__.__name__))

class EmptySentenceError(SentenceError):
    def __init__(self, sentence_str) -> None:
        super().__init__("Empty sentence", sentence_str)

class MalformedSentenceError(SentenceError):
    def __init__(self, err_msg, sentence_str) -> None:
        super().__init__("Malformed sentence", sentence_str)
 
class BadChecksumSentenceError(SentenceError):
    def __init__(self, sentence_str) -> None:
        super().__init__("Bad sentence checksum", sentence_str)

class OuOfOrderSentenceError(SentenceError):
    def __init__(self, sentence_str) -> None:
        super().__init__("Multi sentence progress number out of order", sentence_str)
         
class BadDataSentenceError(SentenceError):
    def __init__(self, err_msg, sentence_str):
        super().__init__("Bad sentence data", sentence_str)

class MissingTimeSentenceError(SentenceError):
    def __init__(self, err_msg, sentence_str):
        super().__init__("Cannot find time information in sentence", sentence_str)



class MessageError(AISParserError):
    def __init__(self, err_msg, sentence_str):
        super().__init__(err_msg)
        self._senetence_str = sentence_str

class CannotDecodeVDMPaylaodError(MessageError):
    def __init__(self, vdm_payload) -> None:
        super().__init__("Impossible decode VDM payload", vdm_payload)  

class MultiLineSentenceError(AISParserError):
    pass
