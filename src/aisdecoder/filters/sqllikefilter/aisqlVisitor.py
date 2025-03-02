# Generated from /home/giampaolo/projects/aisdecoder/src/aisdecoder/filters/sqllikefilter/aisql.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .aisqlParser import aisqlParser
else:
    from aisqlParser import aisqlParser

# This class defines a complete generic visitor for a parse tree produced by aisqlParser.

class aisqlVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by aisqlParser#parse.
    def visitParse(self, ctx:aisqlParser.ParseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by aisqlParser#binaryExpression.
    def visitBinaryExpression(self, ctx:aisqlParser.BinaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by aisqlParser#decimalExpression.
    def visitDecimalExpression(self, ctx:aisqlParser.DecimalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by aisqlParser#boolExpression.
    def visitBoolExpression(self, ctx:aisqlParser.BoolExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by aisqlParser#identifierExpression.
    def visitIdentifierExpression(self, ctx:aisqlParser.IdentifierExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by aisqlParser#notExpression.
    def visitNotExpression(self, ctx:aisqlParser.NotExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by aisqlParser#parenExpression.
    def visitParenExpression(self, ctx:aisqlParser.ParenExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by aisqlParser#comparatorExpression.
    def visitComparatorExpression(self, ctx:aisqlParser.ComparatorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by aisqlParser#comparator.
    def visitComparator(self, ctx:aisqlParser.ComparatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by aisqlParser#binary.
    def visitBinary(self, ctx:aisqlParser.BinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by aisqlParser#bool.
    def visitBool(self, ctx:aisqlParser.BoolContext):
        return self.visitChildren(ctx)



del aisqlParser