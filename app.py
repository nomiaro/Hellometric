import random
import time

from flask import Flask, request

from prometheus_client import (
    Counter,
    generate_latest,
    Histogram,
    REGISTRY,
    Gauge,
)

# [END monitoring_sli_metrics_prometheus_setup]

app = Flask(__name__)
# [START monitoring_sli_metrics_prometheus_create_metrics]
PYTHON_REQUESTS_COUNTER = Counter("python_requests", "total requests")
PYTHON_FAILED_REQUESTS_COUNTER = Counter("python_failed_requests", "failed requests")
PYTHON_LATENCIES_HISTOGRAM = Histogram(
    "python_request_latency", "request latency by path"
)
PYTHON_PARAMETER_TFACTOR = Gauge("python_tfactor", "tfactor", labelnames=['steak_type'])
PYTHON_PARAMETER_MFACTOR = Gauge("python_mfactor", "mfactor", labelnames=['steak_type'])
PYTHON_PARAMETER_THICKNESS = Gauge("python_thickness", "thickness", labelnames=['steak_type'])
PYTHON_PARAMETER_MOISTURE = Gauge("python_moisture", "moisture", labelnames=['steak_type'])
PYTHON_PARAMETER_TEMPERATURE = Gauge("python_temperature", "temperature", labelnames=['steak_type'])
# [END monitoring_sli_metrics_prometheus_create_metrics]

REQUESTS_COUNTER2 = Counter('receive_requests', 'receive_requests', labelnames=['path', 'response_code','factor'])
REQUESTS_COUNTER3 =Counter('complete_requests', 'complete', labelnames=['path', 'response_code','tFactor','thickness','mFactor','moisture','temperature','id','type'])
@app.route("/")
# [START monitoring_sli_metrics_prometheus_latency]
@PYTHON_LATENCIES_HISTOGRAM.time()
# [END monitoring_sli_metrics_prometheus_latency]
def homePage():
    # count request
    # [START monitoring_sli_metrics_prometheus_counts]
    PYTHON_REQUESTS_COUNTER.inc()
    # fail 10% of the time
    if random.randint(0, 100) > 90:
        PYTHON_FAILED_REQUESTS_COUNTER.inc()
        # [END monitoring_sli_metrics_prometheus_counts]
        return ("error!", 500)
    else:
        random_delay = random.randint(0, 5000) / 1000
        # delay for a bit to vary latency measurement
        time.sleep(random_delay)
        return "home page"


# [START monitoring_sli_metrics_prometheus_metrics_endpoint]
@app.route("/metrics", methods=["GET"])
def stats():
    return generate_latest(REGISTRY), 200

@app.route("/thickness", methods=["GET"])
def index():
    factor = request.headers.get('factor')
    REQUESTS_COUNTER2.labels('/thickness', 200,factor).inc()
    return "ok"
@app.route("/moisture", methods=["GET"])
def index2():
    factor = request.headers.get('factor')
    REQUESTS_COUNTER2.labels('/moisture', 200,factor).inc()
    return "ok"
@app.route("/completed", methods=["GET"])
def index3():
    tFactor = request.headers.get('tFactor')
    mFactor = request.headers.get('mFactor')
    thickness = request.headers.get('thickness')
    moisture = request.headers.get('moisture')
    temperature = request.headers.get('temperature')
    type = request.headers.get('type')
    PYTHON_PARAMETER_TFACTOR.labels(type).set(float(tFactor))
    PYTHON_PARAMETER_MFACTOR.labels(type).set(float(mFactor))
    PYTHON_PARAMETER_THICKNESS.labels(type).set(float(thickness))
    PYTHON_PARAMETER_MOISTURE.labels(type).set(float(moisture))
    PYTHON_PARAMETER_TEMPERATURE.labels(type).set(float(temperature))
    id = request.headers.get('id')
    REQUESTS_COUNTER3.labels('/completed', 200,tFactor,thickness,mFactor,moisture,temperature,id,type).inc()
    return "ok"

# [END monitoring_sli_metrics_prometheus_metrics_endpoint]


if __name__ == "__main__":
    app.run(debug=True, host="34.72.100.211", port=8080)