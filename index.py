# OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Auto-Instrumentation
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.jinja2 import Jinja2Instrumentor

import logging
import uuid

from flask import Flask, jsonify, render_template
app = Flask(__name__, static_folder='application/static', template_folder='application/templates')

trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "demo-flask.otel", "service.instance.id": str(uuid.uuid1()), "tag.team": "datacrunch-vercel"})))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

FlaskInstrumentor().instrument_app(app)
Jinja2Instrumentor().instrument()

# Navigation
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

### Add Applications Here #######

# API to calculate the nth prime number and how long it takes
from application.projects.prime import prime
app.register_blueprint(prime)

# API to calculate the nth fibonacci number
from application.projects.fibonacci import fibonacci
app.register_blueprint(fibonacci)

# API to validate credit card numbers
from application.projects.luhn import luhn
app.register_blueprint(luhn)

# Get COVID data and plot on chart
from application.projects.covid import covid
app.register_blueprint(covid)

# Input number to check divisibility
from application.projects.divisibility import divisibility
app.register_blueprint(divisibility)