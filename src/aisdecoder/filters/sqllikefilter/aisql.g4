// grammar aisql;
// 
// prog:   WHERE expr NEWLINE*;
// 
// expr:  
//     |   'cog' OP INT
//     |   'sog' OP INT
//     ;
// 
// NEWLINE : [\r\n]+ ;
// INT     : [0-9]+ ;
// WHERE   : 'WHERE' ;
// WS      : [ \t]+ -> skip ; // toss out whitespace
// OP      : [LT | GT] ;
// GT : '>' ;
// GE : '>=' ;
// LT : '<' ;
// LE : '<=' ;
// EQ : '=' ;

grammar aisql;

parse
 : expression
 ;

expression
 : LPAREN expression RPAREN                       #parenExpression
 | NOT expression                                 #notExpression
 | left=expression op=comparator right=expression #comparatorExpression
 | left=expression op=binary right=expression     #binaryExpression
 | bool                                           #boolExpression
 | IDENTIFIER                                     #identifierExpression
 | DECIMAL                                        #decimalExpression
 | STRING                                         #stringExpression
 ;

comparator
 : GT | GE | LT | LE | EQ
 ;

binary
 : AND | OR
 ;

bool
 : TRUE | FALSE
 ;

AND        : 'AND' ;
OR         : 'OR' ;
NOT        : 'NOT';
TRUE       : 'TRUE' ;
FALSE      : 'FALSE' ;
GT         : '>' ;
GE         : '>=' ;
LT         : '<' ;
LE         : '<=' ;
EQ         : '=' ;
LPAREN     : '(' ;
RPAREN     : ')' ;
DECIMAL    : '-'? [0-9]+ ( '.' [0-9]+ )? ;
STRING     : '"' .*? '"' ; // match anything in "..."
IDENTIFIER : [a-zA-Z_] [a-zA-Z_0-9]* ;
WS         : [ \r\t\u000C\n]+ -> skip;