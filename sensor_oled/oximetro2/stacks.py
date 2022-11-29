from utime import ticks_diff, ticks_us

class Stack_frec():
    def __init__(self):
        self._current = [0,0,0] #Pila para guardar muestras
        self._resample = 0 #control de remuestreo
        self._to = ticks_us() #tiempo de detección inicial
        self.max = 0 #Valor máximo
        self.min = 0 #Valor mínimo
        self.lpm = 0 #frecuencia cardiaca
        #
    def evaluate_sample(self,sample):
        if self._resample < 3: #Condición para realizar remuestreo
            self._resample +=1
        else: #Lógica para detectar max, min y medir lpm
            self._resample = 0 #reinicio remuestreo
            self._current.pop(0) #Sacar la primer muestra de la pila
            self._current.append(sample) #Colocar una nueva muestra al final de la pila
            #condición para minimo
            sentence1 = self._current[0]<self._current[1] and self._current[-1]<self._current[1]
            #condición para máximo
            sentence2 = self._current[0]>self._current[1] and self._current[-1]>self._current[1]
            if self._current[0] < 500: #No hacer nada cuando el dedo no está colocado y poner lpm a cero
                self.lpm = 0
            elif sentence1:
                t = ticks_us()
                dif = ticks_diff(t,self._to)*1e-6 #periodo entre latido y latido
                if dif>0:
                    self.lpm = 60/dif #paso de Hz a lpm
                    self._to = t #actualizar tiempo inicial para medir periodo nuevo
                    self.max = self._current[1] #Guardar valor máximo
            elif sentence2:
                self.min = self._current[1] #Guardar valor minimo
        #
        return self.lpm
