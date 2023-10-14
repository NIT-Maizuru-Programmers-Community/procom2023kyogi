import threading
import time
from matplotlib import pyplot as plt
import math

def showPlt():
    print("showPlt,",threading.current_thread().getName())
    i = 0
    x=[]
    y=[]
    while True:
        math.sin(i)
        x.append(i)
        y.append(math.sin(i))
        plt.plot(x, y)
        i+=0.1
        plt.pause(0.01)

def printLog():
    print("printLog,",threading.current_thread().getName())
    j = 0
    while True:
        print(j, "秒経過")
        j+=1
        time.sleep(1)

# メイン
if __name__ == "__main__":
    # スレッドを作る
    thread1 = threading.Thread(target=showPlt)
    thread2 = threading.Thread(target=printLog)

    # スレッドの処理を開始
    thread1.start()
    thread2.start()