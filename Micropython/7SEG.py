#No acceso al 14 y 16
from machine import Pin, mem32
a,b,c,d,e,f,g = 1,2,3,4,5,6,7,8 #pines
numeros = {
    'uno': (1<<b)|(1<<c),
    'dos': (1<<a)|(1<<b)|(1<<g)|(1<<e)|(1<<d),
    'tres': (1<<a)|(1<<b)|(1<<g)|(1<<c)|(1<<d),
    'cuatro': (1<<b)|(1<<c)|(1<<g)|(1<<f),
    'cinco': (1<<a)|(1<<f)|(1<<g)
}
