from flask import Flask, Response
from prometheus_client import generate_latest, Counter, Histogram
import random
import time

app = Flask(__name__)

REQUEST_COUNT = Counter('app_requests_total', 'Total requests')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

@app.route('/')
def index():
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        time.sleep(random.uniform(0.1, 0.4))
        # Симулируем ~20% ошибок 5xx для алертов и графиков
        if random.random() > 0.8:
            return "Internal Server Error", 500
        return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
