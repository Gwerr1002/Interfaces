#No acceso al 14 y 16
from machine import Pin, mem32
from time import sleep
a,b,c,d,e,f,g = 0,1,2,3,4,5,6 #pines
GPIO_OUT_REG = 0x3FF44004

def corrimientos(*args):
    bin = int()
    for arg in args:
        bin |= 1 << arg
    return bin

numeros = {
    'cero': (1<<a)|(1<<b)|(1<<c)|(1<<d)|(1<<e)|(1<<f),
    'uno': (1<<b)|(1<<c),
    'dos': (1<<a)|(1<<b)|(1<<g)|(1<<e)|(1<<d),
    'tres': (1<<a)|(1<<b)|(1<<g)|(1<<c)|(1<<d),
    'cuatro': (1<<b)|(1<<c)|(1<<g)|(1<<f),
    'cinco': (1<<a)|(1<<f)|(1<<g),
    'seis': (1<<a)|(1<<b)|(1<<c)|(1<<d)|(1<<e)|(1<<g),
    'siete': (1<<a)|(1<<b)|(1<<c),
    'ocho': (1<<a)|(1<<b)|(1<<c)|(1<<d)|(1<<e)|(1<<f)|(1<<g),
    'nueve': (1<<a)|(1<<b)|(1<<c)|(1<<f)|(1<<g),
}

print("ready")

while True:
    for key in numeros:
        mem32[GPIO_OUT_REG] = numeros[key]
        sleep(1)
