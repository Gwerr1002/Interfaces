from machine import Pin, I2C
import ssd1306
from time import sleep
import math
i2c = I2C(1, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
while True:
    for anguloGrados in range(0, 360, 5):                    # Ángulo de giro de la línea del eje (de 0º a 360º en intervalos de 5º)
        anguloRadianes = (math.pi*anguloGrados)/180          # Ángulo de giro de la línea del eje en radianes
        xLinea = int(math.cos(anguloRadianes)*24)            # Coordenada x línea del eje 
        yLinea = int(math.sin(anguloRadianes)*24)            # Coordenada y línea del eje
                                                             # Circunferencia. Radio 25 pixels. Centro (24, 32)
        for anguloGrados in range(0, 360, 5):                # Ángulo de giro de cada pixel de la circunferencia en grados
            anguloRadianes = (math.pi*anguloGrados)/180      # Ángulo de giro de cada pixel de la circunferencia en radianes      
            x = int(math.cos(anguloRadianes)*24)             # Coordenada x pixel circunferencia             
            y = int(math.sin(anguloRadianes)*24)             # Coordenada y pixel circunferencia
            oled.pixel(x+24, y+32, 1)                        # Dibuja cada pixel de la circunferencia
        oled.hline(0, 32, 128, 1)                            # Dibuja la línea horizontal central
        oled.vline(49, 0, 64, 1)                             # Dibuja la línea vertical
        oled.line(24 , 32, xLinea+24, yLinea+32, 1)          # Dibuja la línea del eje. De (24, 32) a (xLinea, yLinea)
        oled.hline(xLinea+24, yLinea+32, 27-xLinea,1)        # Dibuja la línea horizontal giro
        oled.show()                                          # Muestra el resultado
        oled.scroll(1, 0)                                    # Desplaza imagen un pixel a la derecha
        oled.fill_rect(0, 0, 51, 64, 0)
