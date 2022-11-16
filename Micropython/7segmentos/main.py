#No acceso al 14 y 16
from machine import (Pin as PIN, mem32)
from time import sleep
a,b,c,d,e,f,g = 12,13,14,15,16,17,18 #pines a utilizar, se identifica cada segmento con su letra
#Se configuran los pines de los numeros anteriores como salidas
A,B,C,D,E,F,G=PIN(a,PIN.OUT),PIN(b,PIN.OUT),PIN(c,PIN.OUT),PIN(d,PIN.OUT),PIN(e,PIN.OUT),PIN(f,PIN.OUT),PIN(g,PIN.OUT)
GPIO_OUT_REG = 0x3FF44004

def corrimientos(*args):
    bin = int()
    for arg in args: #para cada numero pasado como parámetro se recorre el uno
        bin |= 1 << arg #se enmascara el valor a utilizar con una or
    return bin
'''
Se definen los números con los registros en alto acorde con el segmento
que debe encenderse. se hace el complemento a dos ya que es un
7 segemntos de ánodo común
'''
numeros = [
    ~corrimientos(a,b,c,d,e,f), #0
    ~corrimientos(b,c), #1
    ~corrimientos(a,b,g,e,d), #2
    ~corrimientos(a,b,g,c,d), #3
    ~corrimientos(b,c,g,f), #4
    ~corrimientos(a,f,g,c,d), #5
    ~corrimientos(a,f,c,d,e,g), #6
    ~corrimientos(a,b,c), #7
    ~corrimientos(a,b,c,d,e,f,g), #8
    ~corrimientos(a,b,c,d,f,g) #9
]

print("ready")

while True:
    for num in numeros:
        mem32[GPIO_OUT_REG] = num #asigna el numero que se desea mostrar al registro
        print(num)
        sleep(.5) #tiempo de actualización
