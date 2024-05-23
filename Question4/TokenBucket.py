""" Token Bucket Algorithm """

from flask import Flask, jsonify, request
import time
from collections import defaultdict

class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.tokens = defaultdict(lambda: capacity)
        self.timestamps = defaultdict(lambda: time.time())

    def consume(self, key, tokens=1):
        current_time = time.time()
        elapsed = current_time - self.timestamps[key]

        self.tokens[key] += elapsed * self.rate
        if self.tokens[key] > self.capacity:
            self.tokens[key] = self.capacity

        self.timestamps[key] = current_time

        if self.tokens[key] >= tokens:
            self.tokens[key] -= tokens
            return True
        else:
            return False

    def penalize(self, key, penalty_duration):
        self.timestamps[key] = time.time() + penalty_duration



app = Flask(__name__)

RATE = 15 / 60
CAPACITY = 15
PENALTY_DURATION = 60

token_bucket = TokenBucket(RATE, CAPACITY)

@app.before_request
def limit_requests():
    client_ip = request.remote_addr
    if not token_bucket.consume(client_ip):
        token_bucket.penalize(client_ip, PENALTY_DURATION)
        return jsonify({"error": "Too many requests. Try again later."}), 429

@app.route("/call_me")
def call_me():
    return jsonify({"response": f"Response for {request.args.get('input')}"})

if __name__ == "__main__":
    app.run()
