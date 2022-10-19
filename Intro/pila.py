import re
import sys

#Usando solo pila

def expr_error(expr):
	pila = []
	for char in expr:
		if char == "(":
			pila.append("(")
		elif char == ")":
			try:
				pila.pop()
			except IndexError:
				return "Expresion invalida"
	if pila == []:
		return "Expresion valida"
	else:
		return "Expresion invalida"

#Usando re y pila
def detect_expresion_error_re(expr):
	patron = re.compile("[()]")
	brackets = patron.findall(expr)
	pila = []
	for bracket in brackets:
		if bracket == "(":
			pila.append("(")
		if bracket == ")":
			try:
				pila.pop()
			except IndexError:
				pass
	if pila == []:
		return "Expresion valida"
	else:
		return "Expresion invalida"

#Usando solo re

def error_expr_re(expr):
	p_abrir = len(re.compile("[(]").findall(expr))
	p_cerrar = len(re.compile("[)]").findall(expr))
	if p_abrir != p_cerrar:
		return "Expresión inválida"
	else:
		return "Expresión válida"

if __name__ == "__main__":
	print(expr_error(sys.argv[1]))
