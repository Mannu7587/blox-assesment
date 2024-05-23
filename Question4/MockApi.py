""" Mock Api We'll use Flask to create a simple mock API server that enforces rate limiting."""

from flask import Flask, request, jsonify
import time
from threading import Lock

app = Flask(__name__)

# Rate limiting variables
CALLS_PER_MINUTE = 15
rate_limit_lock = Lock()
call_timestamps = []

@app.route('/call_me', methods=['GET'])
def call_me():
    global call_timestamps

    with rate_limit_lock:
        now = time.time()

        call_timestamps = [timestamp for timestamp in call_timestamps if now - timestamp < 60]

        if len(call_timestamps) < CALLS_PER_MINUTE:
            call_timestamps.append(now)
            return jsonify({"response": f"Response for {request.args.get('input')}"})
        else:
            return jsonify({"error": "Rate limit exceeded"}), 429



if __name__ == '__main__':
    app.run(port=5000)


