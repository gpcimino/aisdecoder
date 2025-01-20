import ais

class AISMessage19:
    @classmethod
    def from_sentence(cls, sentence_payload, padding, receiver_class, time=None):
        try:

            decoded_msg = ais.decode(sentence_payload, padding)
        except ais.DecodeError as ade:
            return None
        decoded_msg['receiver_class'] = receiver_class
        decoded_msg['time']=time
        return cls(decoded_msg)

    def __init__(self, parsed_msg):
        for key, value in parsed_msg.items():
            setattr(self, key, value)

    def message_id(self) -> int:
        return 19            

    
    def write(self, writer):
        self.write_message19(self)     