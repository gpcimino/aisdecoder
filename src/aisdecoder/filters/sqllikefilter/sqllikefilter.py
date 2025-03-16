from abc import abstractmethod
from antlr4 import InputStream, CommonTokenStream # type: ignore

from aisdecoder.filters.filter import Filter
from aisdecoder.ais_kinematic_message import AISKinematicMessage
from aisdecoder.filters.sqllikefilter.aisqlLexer import aisqlLexer
from aisdecoder.filters.sqllikefilter.aisqlParser import aisqlParser
#from aisdecoder.filters.sqllikefilter.aisqlVisitor import aisqlVisitor
from aisdecoder.filters.sqllikefilter.aisql_visitor_impl import AISQLVisitorImpl

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aisdecoder.ais_message import AISMessage

class SQLLikeFilter(Filter):
    def __init__(self, code: str):
        self._code = code

    def match(self, message: "AISMessage") -> bool:
        if not isinstance(message, AISKinematicMessage):
            return False
        
        return self._apply_filter(message)

    def _apply_filter(self, message: "AISKinematicMessage") -> bool:
        input_stream = InputStream(self._code)

        # lexing
        lexer = aisqlLexer(input_stream)
        tokens = CommonTokenStream(lexer)

        # parsing
        parser = aisqlParser(tokens)
        tree = parser.parse()

        # use customized visitor to traverse AST
        visitor = AISQLVisitorImpl(message)
        res = visitor.visit(tree)

        return res
