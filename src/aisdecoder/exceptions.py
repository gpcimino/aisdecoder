class AISParserError(Exception):
    pass

class SentenceError(AISParserError):
    def __init__(self, err_msg, sentence_str):
        super().__init__(err_msg)
        self._senetence_str = sentence_str

class MalformedSenetenceError(SentenceError):
    def __init__(self, err_msg, sentence_str) -> None:
        super().__init__(err_msg, sentence_str)

class BadCheckSumError(SentenceError):
    def __init__(self, sentence_str) -> None:
        super().__init__("Bad sentence checksum", sentence_str)

class SentenceOuOfOrderError(SentenceError):
    def __init__(self, sentence_str) -> None:
        super().__init__("Multi sentence progress number out of order", sentence_str)

class SentenceBadDataError(SentenceError):
    def __init__(self, err_msg, sentence_str):
        super(err_msg, sentence_str)

class MessageError(AISParserError):
    def __init__(self, err_msg, sentence_str):
        super().__init__(err_msg)
        self._senetence_str = sentence_str

class CannotDecodeVDMPaylaodError(MessageError):
    def __init__(self, vdm_payload) -> None:
        super().__init__("Impossible decode VDM payload", vdm_payload)  

class MultiLineSentenceError(AISParserError):
    pass
