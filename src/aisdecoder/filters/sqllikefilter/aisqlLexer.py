# Generated from src/aisdecoder/filters/sqllikefilter/aisql.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,16,110,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,
        13,7,13,2,14,7,14,2,15,7,15,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,2,1,2,
        1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,6,
        1,6,1,6,1,7,1,7,1,8,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,1,12,3,12,
        73,8,12,1,12,4,12,76,8,12,11,12,12,12,77,1,12,1,12,4,12,82,8,12,
        11,12,12,12,83,3,12,86,8,12,1,13,1,13,5,13,90,8,13,10,13,12,13,93,
        9,13,1,13,1,13,1,14,1,14,5,14,99,8,14,10,14,12,14,102,9,14,1,15,
        4,15,105,8,15,11,15,12,15,106,1,15,1,15,1,91,0,16,1,1,3,2,5,3,7,
        4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,12,25,13,27,14,29,15,31,
        16,1,0,4,1,0,48,57,3,0,65,90,95,95,97,122,4,0,48,57,65,90,95,95,
        97,122,3,0,9,10,12,13,32,32,116,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,
        0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,
        0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,
        0,0,27,1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,1,33,1,0,0,0,3,37,1,0,0,
        0,5,40,1,0,0,0,7,44,1,0,0,0,9,49,1,0,0,0,11,55,1,0,0,0,13,57,1,0,
        0,0,15,60,1,0,0,0,17,62,1,0,0,0,19,65,1,0,0,0,21,67,1,0,0,0,23,69,
        1,0,0,0,25,72,1,0,0,0,27,87,1,0,0,0,29,96,1,0,0,0,31,104,1,0,0,0,
        33,34,5,65,0,0,34,35,5,78,0,0,35,36,5,68,0,0,36,2,1,0,0,0,37,38,
        5,79,0,0,38,39,5,82,0,0,39,4,1,0,0,0,40,41,5,78,0,0,41,42,5,79,0,
        0,42,43,5,84,0,0,43,6,1,0,0,0,44,45,5,84,0,0,45,46,5,82,0,0,46,47,
        5,85,0,0,47,48,5,69,0,0,48,8,1,0,0,0,49,50,5,70,0,0,50,51,5,65,0,
        0,51,52,5,76,0,0,52,53,5,83,0,0,53,54,5,69,0,0,54,10,1,0,0,0,55,
        56,5,62,0,0,56,12,1,0,0,0,57,58,5,62,0,0,58,59,5,61,0,0,59,14,1,
        0,0,0,60,61,5,60,0,0,61,16,1,0,0,0,62,63,5,60,0,0,63,64,5,61,0,0,
        64,18,1,0,0,0,65,66,5,61,0,0,66,20,1,0,0,0,67,68,5,40,0,0,68,22,
        1,0,0,0,69,70,5,41,0,0,70,24,1,0,0,0,71,73,5,45,0,0,72,71,1,0,0,
        0,72,73,1,0,0,0,73,75,1,0,0,0,74,76,7,0,0,0,75,74,1,0,0,0,76,77,
        1,0,0,0,77,75,1,0,0,0,77,78,1,0,0,0,78,85,1,0,0,0,79,81,5,46,0,0,
        80,82,7,0,0,0,81,80,1,0,0,0,82,83,1,0,0,0,83,81,1,0,0,0,83,84,1,
        0,0,0,84,86,1,0,0,0,85,79,1,0,0,0,85,86,1,0,0,0,86,26,1,0,0,0,87,
        91,5,34,0,0,88,90,9,0,0,0,89,88,1,0,0,0,90,93,1,0,0,0,91,92,1,0,
        0,0,91,89,1,0,0,0,92,94,1,0,0,0,93,91,1,0,0,0,94,95,5,34,0,0,95,
        28,1,0,0,0,96,100,7,1,0,0,97,99,7,2,0,0,98,97,1,0,0,0,99,102,1,0,
        0,0,100,98,1,0,0,0,100,101,1,0,0,0,101,30,1,0,0,0,102,100,1,0,0,
        0,103,105,7,3,0,0,104,103,1,0,0,0,105,106,1,0,0,0,106,104,1,0,0,
        0,106,107,1,0,0,0,107,108,1,0,0,0,108,109,6,15,0,0,109,32,1,0,0,
        0,8,0,72,77,83,85,91,100,106,1,6,0,0
    ]

class aisqlLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    AND = 1
    OR = 2
    NOT = 3
    TRUE = 4
    FALSE = 5
    GT = 6
    GE = 7
    LT = 8
    LE = 9
    EQ = 10
    LPAREN = 11
    RPAREN = 12
    DECIMAL = 13
    STRING = 14
    IDENTIFIER = 15
    WS = 16

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'AND'", "'OR'", "'NOT'", "'TRUE'", "'FALSE'", "'>'", "'>='", 
            "'<'", "'<='", "'='", "'('", "')'" ]

    symbolicNames = [ "<INVALID>",
            "AND", "OR", "NOT", "TRUE", "FALSE", "GT", "GE", "LT", "LE", 
            "EQ", "LPAREN", "RPAREN", "DECIMAL", "STRING", "IDENTIFIER", 
            "WS" ]

    ruleNames = [ "AND", "OR", "NOT", "TRUE", "FALSE", "GT", "GE", "LT", 
                  "LE", "EQ", "LPAREN", "RPAREN", "DECIMAL", "STRING", "IDENTIFIER", 
                  "WS" ]

    grammarFileName = "aisql.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


