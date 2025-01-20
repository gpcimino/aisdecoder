from aisdecoder.vdm_sentence import MultiLineVDMSentence

class SentenceCorrelationQueue:
    def __init__(self):
        self.sentences = []

    def push(self, sentence):
        if not self.sentences and sentence.is_first():
            self.sentences.append(sentence)
        elif self.sentences and self.sentences[-1].is_before(sentence):
            self.sentences.append(sentence)
        else:
            #log "Sentence progress number out of order"
            #self.errors.add("sentence_progress_number_out_of_order)
            self.flush_sentences()      

    def is_sentence_ready(self):
        if len(self.sentences) == 0:
            return False
        return self.sentences[-1].is_payload_complete()
    
    def flush_sentences(self):
        self.sentences = []
    
    def sentence(self):
        if len(self.sentences) == 0:
            raise Exception("No sentence available")
        #sentence = self.sentence_factory.make_from_sequence(self.sentences)
        if len(self.sentences) == 1:
            sentence = self.sentences[0]
        else:
            sentence = MultiLineVDMSentence(self.sentences)        
        self.flush_sentences()
        return sentence
