/*
  ANTLR4 LaTeX Math Grammar

  Ported from latex2sympy by @augustt198
  https://github.com/augustt198/latex2sympy
  See license in LICENSE.txt
*/

/*
  After changing this file, it is necessary to run `python setup.py antlr`
  in the root directory of the repository. This will regenerate the code in
  `sympy/parsing/latex/_antlr/*.py`.
*/

grammar LaTeX;

options {
    language=Python2;
}

WS: [ \t\r\n]+ -> skip;

THINSPACE: ('\\,' | '\\thinspace') -> skip;
MEDSPACE: ('\\:' | '\\medspace') -> skip;
THICKSPACE: ('\\;' | '\\thickspace') -> skip;
QUAD: '\\quad' -> skip;
QQUAD: '\\qquad' -> skip;
NEGTHINSPACE: ('\\!' | '\\negthinspace') -> skip;
NEGMEDSPACE: '\\negmedspace' -> skip;
NEGTHICKSPACE: '\\negthickspace' -> skip;

ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';

L_PAREN: '(';
R_PAREN: ')';
L_BRACE: '{';
R_BRACE: '}';
L_BRACE_LITERAL: '\\{';
R_BRACE_LITERAL: '\\}';
L_BRACKET: '[';
R_BRACKET: ']';
CMD_LEFT: '\\left' -> skip;
CMD_RIGHT: '\\right' -> skip;

BAR: '|';

FUNC_LIM:  '\\lim';
LIM_APPROACH_SYM: '\\to' | '\\rightarrow' | '\\Rightarrow' | '\\longrightarrow' | '\\Longrightarrow';
FUNC_INT:  '\\int';
FUNC_SUM:  '\\sum';
FUNC_PROD: '\\prod';

FUNC_EXP:  '\\exp';
FUNC_LOG:  '\\log';
FUNC_LN:   '\\ln';
FUNC_SIN:  '\\sin';
FUNC_COS:  '\\cos';
FUNC_TAN:  '\\tan';
FUNC_CSC:  '\\csc';
FUNC_SEC:  '\\sec';
FUNC_COT:  '\\cot';

FUNC_ARCSIN: '\\arcsin';
FUNC_ARCCOS: '\\arccos';
FUNC_ARCTAN: '\\arctan';
FUNC_ARCCSC: '\\arccsc';
FUNC_ARCSEC: '\\arcsec';
FUNC_ARCCOT: '\\arccot';

FUNC_SINH: '\\sinh';
FUNC_COSH: '\\cosh';
FUNC_TANH: '\\tanh';
FUNC_ARSINH: '\\arsinh';
FUNC_ARCOSH: '\\arcosh';
FUNC_ARTANH: '\\artanh';

FUNC_SQRT: '\\sqrt';

CMD_TIMES: '\\times';
CMD_CDOT:  '\\cdot';
CMD_DIV:   '\\div';
CMD_FRAC:  '\\frac';
CMD_BINOM: '\\binom';
CMD_DBINOM: '\\dbinom';
CMD_TBINOM: '\\tbinom';

CMD_MATHIT: '\\mathit';

UNDERSCORE: '_';
CARET: '^';
COLON: ':';

fragment WS_CHAR: [ \t\r\n];
DIFFERENTIAL: 'd' WS_CHAR*? ([a-zA-Z] | '\\' [a-zA-Z]+);

LETTER: [a-zA-Z];
fragment DIGIT: [0-9];
NUMBER:
    DIGIT+ (',' DIGIT DIGIT DIGIT)*
    | DIGIT* (',' DIGIT DIGIT DIGIT)* '.' DIGIT+;

EQUAL: '=';
LT: '<';
LTE: '\\leq';
GT: '>';
GTE: '\\geq';

BANG: '!';

SYMBOL: '\\' [a-zA-Z]+;

math: expr;

expr:
    base=expr CARET exp=expr # Pow
    | expr BANG # Factorial

    | lhs=expr (MUL | CMD_TIMES | CMD_CDOT) rhs=expr # Mul
    | lhs=expr (DIV | CMD_DIV | COLON) rhs=expr # Div
    | lhs=expr ADD rhs=expr # Add
    | lhs=expr SUB rhs=expr # Sub

    | lhs=expr EQUAL rhs=expr # Equals
    | lhs=expr LT rhs=expr # LessThan
    | lhs=expr LTE rhs=expr # LessEqual
    | lhs=expr GT rhs=expr # GreaterThan
    | lhs=expr GTE rhs=expr # GreaterEqual

    | lhs=expr rhs=expr # ImplicitMul
    | special # Specials
    ;

special:
    unary_add | unary_sub
    | paren | absolute_value
    | frac | binom
    | sqrt | log
    | limit | integral
    | summation | product
    | amsmath_func | user_func
    | atom;

atom: (LETTER | SYMBOL) subexpr? | NUMBER | DIFFERENTIAL | mathit;

mathit: CMD_MATHIT L_BRACE mathit_text R_BRACE;
mathit_text: LETTER*;

absolute_value:
    BAR expr BAR;

unary_add: ADD expr;
unary_sub: SUB expr;

paren:
    L_BRACE expr R_BRACE
    | L_PAREN expr R_PAREN
    | L_BRACKET expr R_BRACKET
    | L_BRACE_LITERAL expr R_BRACE_LITERAL;

frac:
    CMD_FRAC L_BRACE
    upper=expr
    R_BRACE L_BRACE
    lower=expr
    R_BRACE;

binom:
    (CMD_BINOM | CMD_DBINOM | CMD_TBINOM) L_BRACE
    n=expr
    R_BRACE L_BRACE
    k=expr
    R_BRACE;

func_normal:
    FUNC_EXP | FUNC_LN
    | FUNC_SIN | FUNC_COS | FUNC_TAN
    | FUNC_CSC | FUNC_SEC | FUNC_COT
    | FUNC_ARCSIN | FUNC_ARCCOS | FUNC_ARCTAN
    | FUNC_ARCCSC | FUNC_ARCSEC | FUNC_ARCCOT
    | FUNC_SINH | FUNC_COSH | FUNC_TANH
    | FUNC_ARSINH | FUNC_ARCOSH | FUNC_ARTANH;

amsmath_func:
    func_normal exp=supexpr?
    (func_arg_parens | func_arg_noparens);

log:
    FUNC_LOG
    (base=subexpr? exp=supexpr? | exp=supexpr? base=subexpr?)
    (func_arg_parens | func_arg_noparens);

sqrt:
    FUNC_SQRT
    (L_BRACKET root=expr R_BRACKET)?
    L_BRACE base=expr R_BRACE;

user_func:
    (LETTER | SYMBOL) subexpr?
    L_PAREN expr (',' expr)* R_PAREN;

integral:
    FUNC_INT (subexpr supexpr | supexpr subexpr)?
    (expr? DIFFERENTIAL);

limit: FUNC_LIM limit_sub expr;
limit_sub:
    UNDERSCORE L_BRACE
    (LETTER | SYMBOL)
    LIM_APPROACH_SYM
    expr (CARET L_BRACE (ADD | SUB) R_BRACE)?
    R_BRACE;

func_args_parens: L_PAREN expr (',' expr)* R_PAREN;
func_arg_parens: L_PAREN expr R_PAREN;

/*
  This is only for handling the ambiguity
  $\sin x \cos y$ -> sin(x)*cos(y) vs sin(x*cos(y))
  And sin(x)*cos(y) is preferred for this.
*/
func_arg_noparens: special;

summation: FUNC_SUM (subeq supexpr | supexpr subeq) expr;
product: FUNC_PROD (subeq supexpr | supexpr subeq) expr;
subexpr: UNDERSCORE (atom | L_BRACE expr R_BRACE);
supexpr: CARET (atom | L_BRACE expr R_BRACE);
subeq: UNDERSCORE L_BRACE expr EQUAL expr R_BRACE;
