
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'left+-left*/rightUMINUSNAME INTEGER BOOL COMMENT ALTER DEF PROC PRINT PRINTLINE SEMICOLON LPAREN RPAREN BREAK REPEATstatement : PROC NAME "(" expression ")"statement : COMMENT statement : PRINTLINEstatement : expression\n    statement : PRINT PRINTLINE\n    expression : expression \'+\' expression\n                  | expression \'-\' expression\n                  | expression \'*\' expression\n                  | expression \'/\' expressionexpression : \'-\' expression %prec UMINUSexpression : \'(\' expression \')\'expression : INTEGERexpression : BOOLexpression : NAMEexpression : DEF "(" NAME "," expression ")"expression : NAME "(" expression ")"expression : ALTER "(" NAME "," expression ")"\n    expression : REPEAT LPAREN expression SEMICOLON BREAK SEMICOLON RPAREN SEMICOLON\n    '
    
_lr_action_items = {'PROC':([0,],[2,]),'COMMENT':([0,],[6,]),'PRINTLINE':([0,8,],[7,22,]),'PRINT':([0,],[8,]),'-':([0,3,4,5,9,10,11,16,17,18,19,20,21,23,26,27,28,29,30,31,32,33,36,37,38,39,40,43,44,46,47,50,],[9,-14,9,19,9,-12,-13,9,19,9,9,9,9,-10,9,9,19,-11,-6,-7,-8,-9,19,19,-16,9,9,19,19,-15,-17,-18,]),'(':([0,3,4,9,12,13,15,16,18,19,20,21,26,27,39,40,],[4,16,4,4,24,25,27,4,4,4,4,4,4,4,4,4,]),'INTEGER':([0,4,9,16,18,19,20,21,26,27,39,40,],[10,10,10,10,10,10,10,10,10,10,10,10,]),'BOOL':([0,4,9,16,18,19,20,21,26,27,39,40,],[11,11,11,11,11,11,11,11,11,11,11,11,]),'NAME':([0,2,4,9,16,18,19,20,21,24,25,26,27,39,40,],[3,15,3,3,3,3,3,3,3,34,35,3,3,3,3,]),'DEF':([0,4,9,16,18,19,20,21,26,27,39,40,],[12,12,12,12,12,12,12,12,12,12,12,12,]),'ALTER':([0,4,9,16,18,19,20,21,26,27,39,40,],[13,13,13,13,13,13,13,13,13,13,13,13,]),'REPEAT':([0,4,9,16,18,19,20,21,26,27,39,40,],[14,14,14,14,14,14,14,14,14,14,14,14,]),'$end':([1,3,5,6,7,10,11,22,23,29,30,31,32,33,38,42,46,47,50,],[0,-14,-4,-2,-3,-12,-13,-5,-10,-11,-6,-7,-8,-9,-16,-1,-15,-17,-18,]),'+':([3,5,10,11,17,23,28,29,30,31,32,33,36,37,38,43,44,46,47,50,],[-14,18,-12,-13,18,-10,18,-11,-6,-7,-8,-9,18,18,-16,18,18,-15,-17,-18,]),'*':([3,5,10,11,17,23,28,29,30,31,32,33,36,37,38,43,44,46,47,50,],[-14,20,-12,-13,20,-10,20,-11,20,20,-8,-9,20,20,-16,20,20,-15,-17,-18,]),'/':([3,5,10,11,17,23,28,29,30,31,32,33,36,37,38,43,44,46,47,50,],[-14,21,-12,-13,21,-10,21,-11,21,21,-8,-9,21,21,-16,21,21,-15,-17,-18,]),')':([3,10,11,17,23,28,29,30,31,32,33,37,38,43,44,46,47,50,],[-14,-12,-13,29,-10,38,-11,-6,-7,-8,-9,42,-16,46,47,-15,-17,-18,]),'SEMICOLON':([3,10,11,23,29,30,31,32,33,36,38,45,46,47,49,50,],[-14,-12,-13,-10,-11,-6,-7,-8,-9,41,-16,48,-15,-17,50,-18,]),'LPAREN':([14,],[26,]),',':([34,35,],[39,40,]),'BREAK':([41,],[45,]),'RPAREN':([48,],[49,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'expression':([0,4,9,16,18,19,20,21,26,27,39,40,],[5,17,23,28,30,31,32,33,36,37,43,44,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> PROC NAME ( expression )','statement',5,'p_statement_proc','Compilador.py',73),
  ('statement -> COMMENT','statement',1,'p_statement_comment','Compilador.py',80),
  ('statement -> PRINTLINE','statement',1,'p_statement_printline','Compilador.py',83),
  ('statement -> expression','statement',1,'p_statement_expr','Compilador.py',85),
  ('statement -> PRINT PRINTLINE','statement',2,'p_statement_print','Compilador.py',90),
  ('expression -> expression + expression','expression',3,'p_expression_binop','Compilador.py',95),
  ('expression -> expression - expression','expression',3,'p_expression_binop','Compilador.py',96),
  ('expression -> expression * expression','expression',3,'p_expression_binop','Compilador.py',97),
  ('expression -> expression / expression','expression',3,'p_expression_binop','Compilador.py',98),
  ('expression -> - expression','expression',2,'p_expression_uminus','Compilador.py',110),
  ('expression -> ( expression )','expression',3,'p_expression_group','Compilador.py',115),
  ('expression -> INTEGER','expression',1,'p_expression_integer','Compilador.py',120),
  ('expression -> BOOL','expression',1,'p_expression_bool','Compilador.py',124),
  ('expression -> NAME','expression',1,'p_expression_name','Compilador.py',129),
  ('expression -> DEF ( NAME , expression )','expression',6,'p_expression_def','Compilador.py',137),
  ('expression -> NAME ( expression )','expression',4,'p_expression_change','Compilador.py',142),
  ('expression -> ALTER ( NAME , expression )','expression',6,'p_expression_math','Compilador.py',150),
  ('expression -> REPEAT LPAREN expression SEMICOLON BREAK SEMICOLON RPAREN SEMICOLON','expression',8,'p_expression_repeat','Compilador.py',161),
]
