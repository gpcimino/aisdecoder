from aisdecoder.ais_message_123 import AISMessage123
from aisdecoder.ais_message_5 import AISMessage5
from aisdecoder.ais_message_18 import AISMessage18

class AllMessagesFactory:
    def can_create(self, msg_id):
        return msg_id in [1,2,3,5,18]
    
    def make(self, msg_id, payload, padding, receiver_class, time):
        if msg_id in [1,2,3]:
            return AISMessage123.from_sentence(payload, padding, receiver_class, time)
        elif msg_id == 5:
            return AISMessage5.from_sentence(payload, padding, receiver_class, time)    
        elif msg_id == 18:
            return AISMessage18.from_sentence(payload, padding, receiver_class, time)            
        else:
            raise ValueError(f"Cannot cretae message with id {msg_id}")
        
class KinematicMessagesFactory:
    def can_create(self, msg_id):
        return msg_id in [1,2,3,18]
    
    def make(self, msg_id, payload, padding, receiver_class, time):
        if msg_id in [1,2,3]:
            return AISMessage123.from_sentence(payload, padding, receiver_class, time)
        elif msg_id == 18:
            return AISMessage18.from_sentence(payload, padding, receiver_class, time)            
        else:
            raise ValueError(f"Cannot cretae message with id {msg_id}")
        

