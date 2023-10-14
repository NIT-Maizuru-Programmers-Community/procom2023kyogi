import threading
import time

# うどんを茹でる関数
def boil_udon():
    print("  ◆スレッド:", threading.currentThread().getName())

    print('  うどんを茹でます。')
    time.sleep(3)
    print('  うどんが茹であがりました。')

# ツユを作る関数
def make_tuyu():
    print("  ◆スレッド:", threading.currentThread().getName())

    print('  ツユをつくります。')
    time.sleep(2)
    print('  ツユができました。')

# メイン
if __name__ == "__main__":
    print("◆スレッド:", threading.currentThread().getName())

    print('うどんを作ります。')

    # スレッドを作る
    thread1 = threading.Thread(target=boil_udon)
    thread2 = threading.Thread(target=make_tuyu)

    # スレッドの処理を開始
    thread1.start()
    thread2.start()

    # スレッドの処理を待つ
    thread1.join()
    thread2.join()

    print('盛り付けます。')
    print('うどんができました。')