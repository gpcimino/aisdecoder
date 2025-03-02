from aisdecoder.filters.sqllikefilter.aisqlVisitor import aisqlVisitor
from aisdecoder.filters.sqllikefilter.aisqlParser import aisqlParser


class AISQLVisitorImpl(aisqlVisitor):

    def __init__(self, ais_message):
        super().__init__()
        self._ais_message = ais_message

    # def visitParse(self, ctx):
    #     return super().visitParse(ctx)

    def visitExpression(self, ctx:aisqlParser.ExpressionContext):
        print("Expression=" + str(ctx.getChild(0)))
        return self.visit(ctx.getChild(0))

    def visitParenExpression(self, ctx:aisqlParser.ParenExpressionContext):
        print("Parentesi=" + str(ctx.expression()))
        return self.visit(ctx.expression())
    
    def visitNotExpression(self, ctx:aisqlParser.NotExpressionContext):
        print("Not=" + str(ctx.expression()))
        return not self.visit(ctx.expression())
    
    def visitBinaryExpression(self, ctx:aisqlParser.BinaryExpressionContext):
        print("Binary=" + str(ctx.op))
        if ctx.op.AND() != None:
            return self.visit(ctx.left) and self.visit(ctx.right)
        elif ctx.op.OR() != None:
            return self.visit(ctx.left) or self.visit(ctx.right)
        else:
            raise Exception("not implemented: binary operator " + ctx.op.getText())
        
    def visitBoolExpression(self, ctx):
        print("Bool=" + str(ctx.getText().strip().lower()))
        bool_literal = ctx.getText().strip().lower()
        if bool_literal == "TRUE":
            return True
        return False

    def visitComparatorExpression(self, ctx):
        print("Compare=" + str(ctx.op))
        if ctx.op.EQ() != None:
            return self.visit(ctx.left) == self.visit(ctx.right)
        elif ctx.op.LE() != None:
            return self.visit(ctx.left) <= self.visit(ctx.right)
        elif ctx.op.GE() != None:
            return self.visit(ctx.left) >= self.visit(ctx.right)
        elif ctx.op.LT() != None:
            return self.visit(ctx.left) < self.visit(ctx.right)
        elif ctx.op.GT() != None:
            return self.visit(ctx.left) > self.visit(ctx.right)
        else:
            raise Exception("not implemented: comparator operator " + ctx.op.getText())

    def visitIdentifierExpression(self, ctx:aisqlParser.IdentifierExpressionContext):
        print("Identifier=" + str(ctx.getText().strip()))
        attr = ctx.getText().strip()
        attr_value = getattr(self._ais_message, attr)
        #print(ctx.getText().strip() + "=" + str(attr_value))
        return attr_value
    


    def visitDecimalExpression(self, ctx):
        print("Decimal=" + str(ctx.getText().strip()))
        return float(ctx.getText())
    
# public Object visitComparatorExpression(SimpleBooleanParser.ComparatorExpressionContext ctx) {
#     if (ctx.op.EQ() != null) {
#       return this.visit(ctx.left).equals(this.visit(ctx.right));
#     }
#     else if (ctx.op.LE() != null) {
#       return asDouble(ctx.left) <= asDouble(ctx.right);
#     }
#     else if (ctx.op.GE() != null) {
#       return asDouble(ctx.left) >= asDouble(ctx.right);
#     }
#     else if (ctx.op.LT() != null) {
#       return asDouble(ctx.left) < asDouble(ctx.right);
#     }
#     else if (ctx.op.GT() != null) {
#       return asDouble(ctx.left) > asDouble(ctx.right);
#     }
#     throw new RuntimeException("not implemented: comparator operator " + ctx.op.getText());
#   }