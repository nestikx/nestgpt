import threading
import time

def timer():
    while True:
        time.sleep(300)

thread = threading.Thread(target = timer)
thread.start()