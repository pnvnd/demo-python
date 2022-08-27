from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LogEmitterProvider
from opentelemetry.sdk._logs import set_log_emitter_provider
from opentelemetry.sdk._logs import LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogProcessor

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.jinja2 import Jinja2Instrumentor

from flask import Flask, jsonify, render_template
app = Flask(__name__, static_folder='application/static', template_folder='application/templates')

import logging
import uuid
serviceId = str(uuid.uuid1())

trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "demo-flask.otel", "service.instance.id": serviceId, "tag.team": "datacrunch-vercel"})))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

log_emitter_provider = LogEmitterProvider(resource=Resource.create({"service.name": "python-flask.otel", "service.instance.id": serviceId, "environment": "local"}))
set_log_emitter_provider(log_emitter_provider)

exporter = OTLPLogExporter(insecure=True)
log_emitter_provider.add_log_processor(BatchLogProcessor(exporter))
log_emitter = log_emitter_provider.get_log_emitter(__name__, "0.1")
handler = LoggingHandler(level=logging.NOTSET, log_emitter=log_emitter)
logging.getLogger().addHandler(handler)

FlaskInstrumentor().instrument_app(app)
Jinja2Instrumentor().instrument()

@app.route("/")
def index():
    return render_template("index.html", title="Flask Web Application")

@app.route('/ping', strict_slashes=False)
def ping():
    return jsonify(ping='pong')

@app.route("/about")
def about():
    return render_template("about.html", title="Datacrunch - About")

@app.route("/statuspage", strict_slashes=False)
def statuspage():
    return render_template("projects/statuspage.html", title="Simple Statuspage")

# API to convert Fahrenheit to Celcius
@app.route("/convertC/<tempF>")
def convertC(tempF):
    tempC = (5/9*(float(tempF))-32)
    logging.info(f"[INFO] Converted {tempF}°F to {tempC:.2f}°C.")
    return f"{tempF}°F is {tempC:.2f}°C."

# API to convert Celcius to Fahrenheit New Comment
@app.route("/convertF/<tempC>")
def convertF(tempC):
    try:
        tempF = 9/5*(float(tempC))+32
        logging.info(f"[INFO] Converted {tempC}°F to {tempF:.2f}°C.")
        return f"{tempC}°C is {tempF:.2f}°F."
    except:
        logging.warning("[WARN] Invalid temperature!")
