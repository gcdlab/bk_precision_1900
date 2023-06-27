import threading
import time

done = False


def worker():
    counter = 0
    while True:
        time.sleep(1)
        counter += 1
        print(counter)


threading.Thread(target=worker, daemon=True).start()

input("Press enter to quit")
done = True

