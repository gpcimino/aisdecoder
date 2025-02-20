
import sys
import ais  # type: ignore




def from_sentence(sentence_payload, padding):
    decoded_msg = ais.decode(sentence_payload, padding)
    print(decoded_msg)

        
if __name__ == "__main__":  
    from_sentence(sys.argv[1], 0)