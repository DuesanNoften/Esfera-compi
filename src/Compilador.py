import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

tokens = [
    'NAME', 'INTEGER', 'BOOL','COMMENT','ALTER','DEF',
    'PROC',   
]

literals = ['=', '+', '-', '*', '/', '(', ')', ',']

# Tokens
t_DEF = 'Def'
t_PROC ='Proc'
t_COMMENT = '[--][a-zA-Z0-9_#$%&/()=!"?\¡¿+~}`{^;,:.@°|¬-]*'
t_NAME = r'[@][a-zA-Z0-9_#]*'
t_ALTER = 'Alter'

def t_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'(True||False)[.]'
    if t.value == "True.":
        t.value=True
    elif t.value == "False.":
        t.value=False
    return t

t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}
procs = {}

def p_statement_proc(p):
    'statement : PROC NAME "(" expression ")"'
    if len(p[2])>1 and len(p[2])<10 :
        procs[p[2]] = p[4]
    else:
        print("Los procesos deben constar de minimo 3 caracteres y maximo 10 \ncontando con el @")

def p_statement_comment(p):
    'statement : COMMENT '
    
    
def p_statement_expr(p):
    'statement : expression'
    print(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_integer(p):
    "expression : INTEGER"
    p[0] = p[1]

def p_expression_bool(p):
    "expression : BOOL"
    p[0] = p[1]


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_expression_def(p):
    'expression : DEF "(" NAME "," expression ")"'
    if len(p[3])>1 and len(p[3])<=10 :
        names[p[3]] = p[5]

def p_expression_change(p):
    'expression : NAME "(" statement ")"'
    names[p[1]] = p[3]

def p_expression_math(p):
    'expression : ALTER "(" NAME "," expression ")"'
    if isinstance(p[5],int) and isinstance(names[p[3]],int) :
        if p[5]=="-":
            names[p[3]]=names[p[3]]-p[5]
        else:
            names[p[3]]=names[p[3]]+p[5]
    else:
        print ("La funcion alter solo cambia el valor de las variables númericas")


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('Esfera-Compi > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
