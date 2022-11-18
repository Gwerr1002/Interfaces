from time import time

class Stack_frec():
    def __init__(self):
        self.current = [0,0,0]
        self.min = 1000
        self.max = 0
        self.min_ready = False
        self.max_ready = False
        self.lpm = 0
        self.to = 0
        self.resample = 0
        #
    def evaluate_sample(self,sample):
        if self.resample < 9:
            self.resample += 1
        elif self.resample == 9:
            self.resample = 0
            self.current.pop(0)
            self.current.append(sample)
            print(self.current)
            if self.current[0]>self.current[1] and self.current[-1]>self.current[1] and self.current[1]<self.min:
                print("a")
                self.to = time()
                self.min = self.current[1]
                self.min_ready , self.max_ready= True, False
            elif self.current[0]<self.current[1] and self.current[-1]<self.current[1] and self.current[1]>self.max and self.min_ready:
                print("b")
                self.max_ready = True
                #
            if self.max_ready and self.min_ready and sample > (self.min-1) and sample < (self.min+1):
                print("c")
                self.lpm = 60/(time()-self.to)
                self.reboot()
                #print(f"min {self.min_ready}",f"max {self.max_ready}")
        #
        return self.lpm

    def reboot(self):
        self.max_ready, self.min_ready = False, False
        self.max, self.min = 0, 1000
