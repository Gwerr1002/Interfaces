from readESP32 import YoumuESP32
from adq import AdqSave, graf, show
from matplotlib.animation import FuncAnimation
from threading import Thread

AS = AdqSave()
collectESP32 = YoumuESP32(AS)
Graphic = graf()

if __name__ == "__main__":
    try: 
        anim = FuncAnimation(fig, graf.update_graf, fargs=(AS.dev1['ay'],AS.dev2['ay']),interval=50, blit=False)
        Thread(target=collectESP32.start).start()
    except KeyboardInterrupt:
        collectESP32.stop()
        AS.s_device1()
        AS.s_device2()
