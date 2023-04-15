import ply.lex as lex
import sys
import codecs
sys.path.insert(0, "../..")


if sys.version_info[0] >= 3:
    raw_input = input

toks = []
tokens = [
    'NAME', 'INTEGER', 'BOOL','COMMENT','ALTER','DEF',
    'PROC', 'PRINT', 'PRINTLINE', 'SEMICOLON', 'COMMA','TYPE', 'NOT', 'LPAREN',
    'RPAREN', 'BREAK', 'REPEAT', 'UNTIL', 'WHILE', 'MOVER', 'ALEATORIO',
    'MOVIMIENTO', 'HORN', 'GT', 'LT', 'GTE', 'LTE', 'NE', 'EQUAL',
    'ISTRUE', 'CASE', 'WHEN', 'THEN', 'ELSE'
]

literals = ['=', '+', '-', '*', '/', '(', ')', ',']

#Estos son los caracteres que acepta cada uno de los tokens, algunos aceptando
#carecteres de manera indefinida como t_COMMENT, y otros solo aceptando palabras
#predefinidas como t_DEF
t_DEF = 'Def'
t_PROC ='Proc'
t_COMMENT = '[--][a-zA-Z0-9_#$%&/()=!"?\¡¿+~}`{^;,:.@°|¬-]*[;]'
t_NAME = r'[@][a-zA-Z0-9_#]*'
t_ALTER = 'Alter'
t_PRINT = r'\=>'
t_PRINTLINE='[("][ a-zA-z0-9_#$%&/()=!"?\¡¿+~}`{^;,:.@°|¬-]*[")]'
t_SEMICOLON = r'\;'
t_LPAREN = r'\('
t_COMMA = r'\,'
t_RPAREN = r'\)'
t_BREAK = 'break'
t_REPEAT = 'Repeat'
t_UNTIL = 'Until'
t_WHILE = 'While'
t_MOVER = 'Mover'
t_ALEATORIO = 'Aleatorio'
t_MOVIMIENTO = r'ATR|ADL|ADE|AIZ|IZQ|DER|DDE|DIZ|SPINL|SPINR'
t_HORN = 'HORN' 
t_GT = '>'
t_LT = '<'
t_LTE = '<='
t_GTE = '>='
t_NE = '<>'
t_EQUAL = '=='
t_ISTRUE = "IsTrue"
t_CASE = "Case"
t_WHEN = "When"
t_THEN = "Then"
t_ELSE = "Else"
t_NOT = "Not"


#Reglas lexicas para el token de integer, además de convertir el texto dado
#a entero.
def t_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

#Reglas lexicas para el token de bool, además de convertir el texto dado
#a su respectivo valor booleano.
def t_BOOL(t):
    r'(True|False)'
    if t.value == "True":
        t.value=True
    elif t.value == "False":
        t.value=False
    return t

##Reglas lexicas para el token de Type, el cual devuelve como resultado el
#texto dado.
def t_TYPE(t):
    r'(integer|boolean)'
    return t


t_ignore = " \t"

#Encargado de manejar la creación de nuevas lineas, además de númerarlas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

#Encargado de manejar los errores lexicos al ingresar un caracter invalido
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



lexer = lex.lex()

#Indica el orden de precedencia entre las operaciones
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    ('right', 'CASE', 'WHEN')
)


#Se encarga de abrir y leer el archivo que se le indique
def read_File(dir):
    fp = codecs.open(dir, "r", "utf-8")
    cadena = fp.read()
    fp.close()
    lexer.input(cadena)
    while True:
        tok = lexer.token()
        if not tok: break
        toks.append(str(tok))
    return toks
def cleartoks():
    toks.clear()
