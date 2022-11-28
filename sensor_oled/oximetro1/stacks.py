from time import time_ns

class Stack_frec():
    def __init__(self):
        self._current = [0,0,0]
        self._resample = 0
        self._to = time_ns()
        self.max = 0
        self.min = 0
        self.lpm = 0
        #
    def evaluate_sample(self,sample):
        if self._resample < 19:
            self._resample +=1
        else:
            self._resample = 0
            self._current.pop(0)
            self._current.append(sample)
            sentence1 = self._current[0]<self._current[1] and self._current[-1]<self._current[1]
            sentence2 = self._current[0]>self._current[1] and self._current[-1]>self._current[1]
            if sentence1:
                t = time_ns()
                dif = (t-self._to)*1e-9
                if dif>0:
                    self.lpm = 3*60/dif
                    self._to = t
                    self.max = self._current[1]
            elif sentence2:
                self.min = self._current[1]
            elif self._current[0] < 200:
                self.lpm = 0
        #
        return self.lpm
