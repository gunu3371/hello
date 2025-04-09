import threading
import queue
import random
import time

class Producer(threading.Thread):
    def __init__(self, queue, event):
        super().__init__()
        self.queue = queue
        self.event = event

    def run(self):
        while not self.event.is_set():
            item = random.randint(1, 100)
            self.queue.put(item)
            print(f"Produced: {item}")
            time.sleep(random.uniform(0.1, 0.5))
        print("Producer stopped.")

class Consumer(threading.Thread):
    def __init__(self, queue, event):
        super().__init__()
        self.queue = queue
        self.event = event

    def run(self):
        while not self.event.is_set() or not self.queue.empty():
            try:
                item = self.queue.get(timeout=0.1)
                print(f"Consumed: {item}")
                self.queue.task_done()
            except queue.Empty:
                continue
        print("Consumer stopped.")

def main():
    q = queue.Queue()
    stop_event = threading.Event()

    producer = Producer(q, stop_event)
    consumer = Consumer(q, stop_event)

    producer.start()
    consumer.start()

    try:
        time.sleep(5)  # Let the threads run for 5 seconds
    finally:
        stop_event.set()
        producer.join()
        consumer.join()

    print("All threads stopped.")

if __name__ == "__main__":
    main()