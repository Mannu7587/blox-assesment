""" Manage 20 calls """

import time
import threading
from queue import Queue
import requests

class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.tokens = max_calls
        self.lock = threading.Lock()
        self.last_refill = time.time()

    def _refill_tokens(self):
        now = time.time()
        elapsed = now - self.last_refill
        if elapsed >= self.period:
            self.tokens = self.max_calls
            self.last_refill = now

    def acquire(self):
        with self.lock:
            self._refill_tokens()
            if self.tokens > 0:
                self.tokens -= 1
                return True
            return False

def call_me(input):
    try:
        response = requests.get(f'http://127.0.0.1:5000/call_me?input={input}')
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.json()}")
    except Exception as e:
        print(f"Exception during API call: {e}")

rate_limiter = RateLimiter(15, 60)
request_queue = Queue()

def worker():
    while True:
        input = request_queue.get()
        if rate_limiter.acquire():
            call_me(input)
        else:
            time.sleep(1)
            request_queue.put(input)
        request_queue.task_done()

for _ in range(5):
    threading.Thread(target=worker, daemon=True).start()

start_time = time.time()
for i in range(20):
    request_queue.put(f"Request {i}")

request_queue.join()
end_time = time.time()

total_time = end_time - start_time
print(f"Total time taken to make 20 calls: {total_time:.2f} seconds")
