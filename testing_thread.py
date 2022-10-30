import threading
import time

def my_long_function():
    while 1:
        print("runs in background")
        time.sleep(1)

long_thread = threading.Thread(target=my_long_function)
long_thread.start()

while 1:
    print("Running in foreground")
    time.sleep(3)