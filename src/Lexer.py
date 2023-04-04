import ply.lex as lex
import sys
import codecs
sys.path.insert(0, "../..")


if sys.version_info[0] >= 3:
    raw_input = input

toks = []
tokens = [
    'NAME', 'INTEGER', 'BOOL','COMMENT','ALTER','DEF',
    'PROC', 'PRINT', 'PRINTLINE', 'SEMICOLON', 'LPAREN',
    'RPAREN', 'BREAK', 'REPEAT'
]

literals = ['=', '+', '-', '*', '/', '(', ')', ',']

def t_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'(True|False)'
    if t.value == "True":
        t.value=True
    elif t.value == "False":
        t.value=False
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_DEF = 'Def'
t_PROC ='Proc'
t_COMMENT = '[--][a-zA-Z0-9_#$%&/()=!"?\¡¿+~}`{^;,:.@°|¬-]*'
t_NAME = r'[@][a-zA-Z0-9_#]*'
t_ALTER = 'Alter'
t_PRINT = r'\=>'
t_PRINTLINE='[("][a-zA-z0-9_#$%&/()=!"?\¡¿+~}`{^;,:.@°|¬-]*[")]'
t_SEMICOLON = r'\;'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_BREAK = 'break'
t_REPEAT = 'Repeat'

lexer = lex.lex()

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

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