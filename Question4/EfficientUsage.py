"""efficient usage"""
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
    strt_time = time.time()
    while True:
        input = request_queue.get()
        if rate_limiter.acquire():
            call_me(input)
        else:
            crr_time = time.time()
            t = 60-(crr_time - strt_time)+1
            time.sleep(t)
            request_queue.put(input)
        request_queue.task_done()

for _ in range(5):
    threading.Thread(target=worker, daemon=True).start()

for i in range(30):
    request_queue.put(f"Request {i}")

request_queue.join()

