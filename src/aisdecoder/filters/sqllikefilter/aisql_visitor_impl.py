from aisdecoder.filters.sqllikefilter.aisqlVisitor import aisqlVisitor
from aisdecoder.filters.sqllikefilter.aisqlParser import aisqlParser


class AISQLVisitorImpl(aisqlVisitor):

    def __init__(self, ais_message):
        super().__init__()
        self._ais_message = ais_message

    # def visitParse(self, ctx):
    #     return super().visitParse(ctx)

    def visitExpression(self, ctx:aisqlParser.ExpressionContext):
        #print("Expression=" + str(ctx.getChild(0)))
        return self.visit(ctx.getChild(0))

    def visitParenExpression(self, ctx:aisqlParser.ParenExpressionContext):
        #print("Parentesi=" + str(ctx.expression()))
        return self.visit(ctx.expression())
    
    def visitNotExpression(self, ctx:aisqlParser.NotExpressionContext):
        #print("Not=" + str(ctx.expression()))
        return not self.visit(ctx.expression())
    
    def visitBinaryExpression(self, ctx:aisqlParser.BinaryExpressionContext):
        #print("Binary=" + str(ctx.op))
        if ctx.op.AND() != None:
            return self.visit(ctx.left) and self.visit(ctx.right)
        elif ctx.op.OR() != None:
            return self.visit(ctx.left) or self.visit(ctx.right)
        else:
            raise Exception("not implemented: binary operator " + ctx.op.getText())
        
    def visitBoolExpression(self, ctx):
        #print("Bool=" + str(ctx.getText().strip().lower()))
        bool_literal = ctx.getText().strip().lower()
        if bool_literal == "true":
            return True
        return False

    def visitComparatorExpression(self, ctx):
        #print("Compare=" + str(ctx.op))
        left = self.visit(ctx.left)
        if left == None:
            return False
        right = self.visit(ctx.right)
        if right == None:
            return False
        if ctx.op.EQ() != None:
            return left == right
        elif ctx.op.LE() != None:
            return left <= right
        elif ctx.op.GE() != None:
            return left >= right
        elif ctx.op.LT() != None:
            return left < right
        elif ctx.op.GT() != None:
            return left > right
        else:
            raise Exception("not implemented: comparator operator " + ctx.op.getText())

    def visitIdentifierExpression(self, ctx:aisqlParser.IdentifierExpressionContext):
        attr = ctx.getText().strip()

        if attr == "course_over_ground" or attr == "cog":
            return self._ais_message.course_over_ground()
        elif attr == "speed_over_ground" or attr == "sog":
            return self._ais_message.speed_over_ground()
        elif attr == "true_heading":
            return self._ais_message.true_heading()
        elif attr == "position_accuracy":
            return self._ais_message.position_accuracy()
        elif attr == "rate_of_turn" or attr == "rot":
            return self._ais_message.rate_of_turn()
        elif attr == "message_id" or attr == "id":
            return self._ais_message.message_id()
        elif attr == "name":
            if self._ais_message.message_id() in  [1,2,3]:
                if self._ais_message.static_msg is None:
                    return None
                return self._ais_message.static_msg.name()           
            elif self._ais_message.message_id() == 19:
                return self._ais_message.name()                  
        else:
            raise Exception("Unknown attribute: " + attr)
        # attr = ctx.getText().strip()
        # try:
        #     attr_value = getattr(self._ais_message, attr)
        # except AttributeError:
        #     attr_value = getattr(self._ais_message, attr)()
        # #print(ctx.getText().strip() + "=" + str(attr_value))
        # return attr_value

    def visitDecimalExpression(self, ctx):
        #print("Decimal=" + str(ctx.getText().strip()))
        return float(ctx.getText())
 
    def visitStringExpression(self, ctx):
        return ctx.getText()[1:-1] # remove the intial and ending double quotes
    
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