import ply.yacc as yacc
import os
import codecs
import re
from Lexer import tokens
#EV3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import random

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

#Ev3 initializing
ev3 = EV3Brick()
#Motors initializing 
leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)
#Motor driver initializing
carBall = DriveBase(leftMotor, rightMotor, wheel_diameter = 55.5, axle_track = 104)

def p_symbols(p):
    'symbol : Body'
    p[0] = p[1]

start = 'Body'
def stop():
    carBall.stop()
    leftMotor.brake()
    rightMotor.brake()
    carBall.settings(straight_speed=3000,straight_acceleration=1500)

def p_statement_proc(p):
    'statement : PROC NAME "(" expression ")"'
    if len(p[2])>1 and len(p[2])<10 :
        procs[p[2]] = p[4]
    else:
        p[0]="Los procesos deben constar de minimo 3 caracteres y maximo 10 \ncontando con el @"

def p_statement_comment(p):
    'statement : COMMENT '

def p_statement_printline(p):
    'statement : PRINTLINE'

def p_statement_expr(p):
    '''
    statement : expression
              | expression statement
              |
    '''
    if len(p)==2:
        p[0]=(p[1])
    if len(p)==3:
        p[0]=(p[1],p[2])

def p_statement_print(p):
    '''
    statement : PRINT PRINTLINE
    '''
    p[0]=p[2]

def p_statement_case(p):#el statement del case
    '''statement : CASE WHEN expression statementt statementE''' #La gramatica para el statement

    if p[3]:# Verifica si la expression es verdadera.
        print(p[5])
        p[0] = p[5]

def p_statement_then(p):#el then del case when y del case x when
    """ statementt : THEN statement """ #La gramatica para el then
    if p[-1]: # verifica si la condicion es real.
        p[0] = p[2]
    else:# en caso de que no sea verdadera la condicion
        a = p[2] #Se verifica que se reciba una lista
        if isinstance(a, list):
            b = a[0]
            c = a[1]
            if type(c[1]) == int:
                names[b] = names[b][1] - c #elimina los cambios a la variable
            else:
                names.pop(b) #Elimina la variable


def p_statement_cases(p): #el cases de when
    """ statement : CASE expression """
    p[1] = p[2]
    p[0] = p[2]

def p_statement_when(p):# el statement when
    """statement : statement WHEN expression then statement statementE"""

    if p[1] == p[3]:#verifica que el case sea valido
        print(p[5])
        p[0] = p[5]
    else:
        p[0] = p[1]

def p_statement_else(p): #Statement de else
    '''statementE : ELSE statement
                | empty'''

    if type(p[1]) == str: #Verifica que no sea vacio
        p[0] == p[2]
def p_statement_aleatorio(p):
    '''
    statement : ALEATORIO LPAREN RPAREN
    '''
    i = 10
    while i>0:
        a = random.randint(1, 8)
        
        if a == 1:
            carBall.straight(-200)
            stop()
        elif a == 2:
            carBall.straight(200)
            stop()
        elif a == 3:
            carBall.turn(45)
            stop()
            carBall.straight(200)
            stop()
            carBall.turn(-45)
            stop()
        elif a == 4:
            carBall.turn(-45)
            stop()
            carBall.straight(-200)
            stop()
            carBall.turn(45)
            stop()

        elif a == 5:
            carBall.turn(90)
            stop()
            carBall.straight(200)
            stop()
            carBall.turn(-90)
            stop()
        elif a == 6:
            carBall.turn(-90)
            stop()
            carBall.straight(200)
            stop()
            carBall.turn(90)
            stop()
        elif a == 7:
            carBall.turn(-45)
            stop()
            carBall.straight(200)
            stop()
            carBall.turn(45)
            stop()
        elif a == 8:
            carBall.turn(45)
            stop()
            carBall.straight(200)
            stop()
            carBall.turn(-45)
            stop()

def p_statement_horn(p):
    '''
    statement : HORN LPAREN RPAREN
    '''
    ev3.speaker.beep()


def p_statement_mover(p):
    '''
    statement : MOVER LPAREN MOVIMIENTO RPAREN SEMICOLON
    '''
    if p[3].value == 'ATR':
        print("La esfera va a moverse hacia atras")
        p[0]="La esfera va a moverse hacia atras"
        carBall.straight(-200)
        stop()
    
    elif p[3].value == 'ADL':
        print("La esfera va a moverse hacia delante")
        p[0]="La esfera va a moverse hacia delante"
        carBall.straight(200)
        stop()
    
    elif p[3].value == 'ADE':
        print("La esfera va a moverse hacia atras a la derecha")
        p[0]="La esfera va a moverse hacia atras a la derecha"
        carBall.turn(45)
        stop()
        carBall.straight(200)
        stop()
        carBall.turn(-45)
        stop()
    
    elif str(p[3]) == 'AIZ':
        print("La esfera va a moverse hacia atras a la izquierda")
        p[0]="La esfera va a moverse hacia atras a la izquierda"
        carBall.turn(-45)
        stop()
        carBall.straight(-200)
        stop()
        carBall.turn(45)
        stop()
    
    elif str(p[3]) == 'IZQ':
        print("La esfera va a moverse hacia la izquierda")
        p[0]="La esfera va a moverse hacia la izquierda"
        carBall.turn(90)
        stop()
        carBall.straight(200)
        stop()
        carBall.turn(-90)
        stop()

    elif str(p[3]) == 'DER':
        print("La esfera va a moverse hacia la derecha")
        p[0]="La esfera va a moverse hacia la derecha"
        carBall.turn(-90)
        stop()
        carBall.straight(200)
        stop()
        carBall.turn(90)
        stop()

    elif str(p[3]) == 'DDE':
        print("La esfera va a moverse hacia delante a la derecha")
        p[0]="La esfera va a moverse hacia delante a la derecha"
        carBall.turn(-45)
        stop()
        carBall.straight(200)
        stop()
        carBall.turn(45)
        stop()
    
    elif str(p[3]) == 'DIZ':
        print("La esfera va a moverse hacia delante a la izquierda")
        p[0]="La esfera va a moverse hacia delante a la izquierda"
        carBall.turn(45)
        stop()
        carBall.straight(200)
        stop()
        carBall.turn(-45)
        stop()

    elif str(p[3]) == 'SPINL':
        print("La esfera va a dar varias vueltas hacia la izquierda")
        p[0]="La esfera va a dar varias vueltas hacia la izquierda"
        carBall.turn(-1080)
        stop()

    elif str(p[3]) == 'SPINR':
        print("La esfera va a dar varias vueltas hacia la derecha")
        p[0]="La esfera va a dar varias vueltas hacia la derecha"
        carBall.turn(1080)
        stop()


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

# Manda la comparacion a hacer
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

def p_expression_compr(p): #Realiza las comapraciones
    '''expression : expression relation expression'''

    if type(p[1]) == int and type(p[3]) == int:# Verifica que sean ints los datos
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
        p[0]="Compara valores no validos"

def p_expression_istrue(p): # Verifica que la variable sea True
    '''expression : ISTRUE LPAREN expression RPAREN SEMICOLON '''

    if isinstance([3], bool): #Verifica que la variable sea bool
        if p[3] == True:
            p[0] = True
            print("True")
        else:
            p[0] = False
            print("False")
    else:
        p[0]="IsTrue con formatos no validos "
def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_expression_group(p):
    "expression : LPAREN expression RPAREN "
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
        p[0] = names[p[1]][1]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_expression_def(p):
    '''expression : DEF LPAREN NAME COMMA TYPE COMMA INTEGER RPAREN SEMICOLON
                  | DEF LPAREN NAME COMMA TYPE COMMA BOOL RPAREN SEMICOLON
                  | DEF LPAREN NAME COMMA TYPE RPAREN SEMICOLON '''
    if len(p[3])>1 and len(p[3])<=10 :
        if p[6]== ',':
            if (p[5]=='integer'):
                if isinstance(p[7],int):
                    names[p[3]] = [p[5],p[7]]
                else:
                    print ("Error, tipo de la variable no coincide con el valor dado")
            elif (p[5]=='boolean'):
                if isinstance(p[7],bool):
                    names[p[3]] = [p[5],p[7]]
                else:
                    print ("Error, tipo de la variable no coincide con el valor dado")
        elif p[6]==')':
            names[p[3]] = [p[5],None]

def p_expression_change(p):
    'expression : NAME "(" expression ")"'
    if names[p[1]][0]=="integer":
        if names[p[1]]!=None and isinstance(names[p[1]][1], int)^isinstance(p[3],bool):
            names[p[1]][1]=p[3]
    elif names[p[1]][0]=="boolean":
        if names[p[1]]!=None and (names[p[1]][0]=="boolean") ^ isinstance(p[3],int) :
            names[p[1]][1]=p[3]
    else:
        print("El valor asignado a la variabl debe ser del mismo tipo")

def p_expression_not(p):
    'expression : NOT "(" NAME ")"'
    temp=names[p[3]][1]
    if temp:
        names[p[3]][1]=False
    else:
        names[p[3]][1]=True


def p_expression_math(p):
    'expression : ALTER "(" NAME "," expression ")"'
    if isinstance(p[5], int) and isinstance(names[p[3]][1], int):

        names[p[3]][1] = names[p[3]][1] + p[5]
    else:
        print("La funcion alter solo cambia el valor de las variables númericas")

def p_expression_repeat(p):
    '''
    expression : REPEAT LPAREN expression SEMICOLON BREAK SEMICOLON RPAREN SEMICOLON
    '''
    p[0]=(p[1],p[3])

def p_expression_repeat_error(p):
    '''
    expression : REPEAT LPAREN expression SEMICOLON RPAREN SEMICOLON
    '''
    p[0]="Error expected break not found"

def p_expression_until(p):
    '''
    expression : UNTIL LPAREN expression RPAREN statement SEMICOLON
    '''
    p[0]=(p[1],p[3],p[5])

def p_expression_until_error(p):
    '''
    expression :  UNTIL LPAREN expression RPAREN
          |  UNTIL LPAREN expression RPAREN SEMICOLON
    '''
    p[0]="Error expected condition not found"

def p_statement_while(p):
    '''
    statement : WHILE LPAREN expression RPAREN LPAREN statement RPAREN SEMICOLON
    '''
    print(p[3])
    if p[3]==True:
        p[0]=(p[1],p[6])

def p_expression_Body(p):
    '''
    Body : expression statement expression
         | expression statement
         | statement expression
         | statement
         | statement statement
         | statement expression statement
         | expression expression
    '''

    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]


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