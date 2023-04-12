import ply.yacc as yacc
import os
import codecs
import re
from Lexer import tokens

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    ('right', 'CASE', 'WHEN')
)

run_flag = True
pars = []
errors = []
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

def p_statement_printline(p):
    'statement : PRINTLINE'

def p_statement_expr(p):
    'statement : expression'
    p[0]=p[1]

def p_statement_print(p):
    '''
    statement : PRINT PRINTLINE
    '''
    p[0]=p[2]

def p_statement_case(p):
    '''statement : CASE WHEN expression THEN statement'''

    if p[3]:
        print('Esto es para separar')
        print(p[5])
        p[0] = p[5]

def p_statement_cases(p):
    """ statement : CASE expression """
    p[1] = p[2]
    p[0] = p[2]

def p_statement_when(p):
    """statement : statement WHEN expression THEN statement"""

    if p[1] == p[3]:
        print("vamos bien")
        print(p[5])
        p[0] = p[5]
    else:
        p[0] = p[1]
        print("no entro")

def statement_else(p):
    '''statement : ELSE statement
                    | empty'''

    print(p[1])
    p[0] = p[1]
def p_statement_aleatorio(p):
    '''
    statement : ALEATORIO LPAREN RPAREN
    '''
def p_statement_mover(p):
    '''
    statement : MOVER LPAREN MOVIMIENTO RPAREN
    '''
    if p[3].value == 'ATR':
        print("Aqui va a moverse hacia atras")
    
    elif p[3].value == 'ADL':
        print("Aqui va a moverse hacia delante")
    
    elif p[3].value == 'ADE':
        print("Aqui va a moverse hacia atras a la derecha")
    
    elif p[3].value == 'AIZ':
        print("Aqui va a moverse hacia atras a la izquierda")
    
    elif p[3].value == 'IZQ':
        print("Aqui va a moverse hacia la izquierda")

    elif p[3].value == 'DER':
        print("Aqui va a moverse hacia la derecha")

    elif p[3].value == 'DDE':
        print("Aqui va a moverse hacia delante a la derecha")
    
    elif p[3].value == 'DIZ':
        print("Aqui va a moverse hacia delante a la izquierda")

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

def p_relation_GT(p):
    """ relation : GT """
    p[0] = '>'

def p_relation_LT(p):
    """ relation : LT """
    p[0] = '<'

def p_relation_GTE(p):
    """ relation : GTE """
    p[0] = '>='

def p_relation_LTE(p):
    """ relation : LTE """
    p[0] = '<='

def p_relation_NE(p):
    """ relation : NE """
    p[0] = '<>'

def p_relation_EQUAL(p):
    ''' relation : EQUAL '''
    p[0] = '=='

def p_expression_compr(p):
    '''expression : expression relation expression'''

    if p[1] == int and p[2] == int:
        if p[2] == '<':
            print(p[1] < p[3])
            p[0] = p[1] < p[3]
        elif p[2] == '>':
            print(p[1] > p[3])
            p[0] = p[1] > p[3]
        elif p[2] == '<=':
            print(p[1] <= p[3])
            p[0] = p[1] <= p[3]
        elif p[2] == '>=':
            print(p[1] >= p[3])
            p[0] = p[1] >= p[3]
        elif p[2] == '<>':
            print(p[1] != p[3])
            p[0] = p[1] != p[3]
        elif p[2] == '==':
            print(p[1] == p[3])
            p[0] = p[1] == p[3]
        else:
            print("no sirve")
    else:
        print("Compara valores no validos")

def p_expression_istrue(p):
    '''expression : ISTRUE '(' expression ')' '''

    if p[3] == bool:
        if p[3] == True:
            p[0] = True
            print("True")
        else:
            p[0] = False
            print("False")
    else:
        print("IsTrue con formatos no validos ")
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
    'expression : NAME "(" expression ")"'
    breakpoint()
    if names[p[1]]!=None and isinstance(names[p[1]], int)^isinstance(p[3],bool):
        names.update({p[1]:p[3]})
    else:
        print("El valor asignado a la variable debe ser del mismo tipo")

def p_expression_math(p):
    'expression : ALTER "(" NAME "," expression ")"'
    if isinstance(p[5],int) and isinstance(names[p[3]],int) :
        if p[5]=="-":
            names[p[3]]=names[p[3]]-p[5]
        else:
            names[p[3]]=names[p[3]]+p[5]
    else:
        print ("La funcion alter solo cambia el valor de las variables númericas")

def p_expression_repeat(p):
    '''
    expression : REPEAT LPAREN expression SEMICOLON BREAK SEMICOLON RPAREN SEMICOLON
    '''
    p[0]=(p[1],p[3])

def p_expression_repeat_error(p):
    '''
    expression : REPEAT LPAREN expression SEMICOLON RPAREN SEMICOLON
    '''
    print("Error expected break not found")

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

def readFile(dir, run):
    if not run:
        run_flag = False
    fp = codecs.open(dir, "r", "utf-8")
    cadena = fp.read()
    parser = yacc.yacc()
    fp.close()
    par = parser.parse(cadena)
    pars.append(par)
    return pars

def clearpars():
    errors.clear()
    pars.clear()