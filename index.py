from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.jinja2 import Jinja2Instrumentor

from flask import Flask, jsonify, render_template
app = Flask(__name__)

import uuid
serviceId = str(uuid.uuid1())

trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "demo-flask.otel", "service.instance.id": serviceId, "tag.team": "datacrunch-vercel"})))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

FlaskInstrumentor().instrument_app(app)
Jinja2Instrumentor().instrument()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/ping', strict_slashes=False)
def ping():
    return jsonify(ping='pong')

@app.route('/hello')
def hello():
    return render_template('hello.html')

# API to convert Fahrenheit to Celcius
@flaskapp.route("/convertC/<tempF>")
def convertC(tempF):
    tempC = (5/9*(float(tempF))-32)
#    logging.info(f"[INFO] Converted {tempF}°F to {tempC:.2f}°C.")
    return f"{tempF}°F is {tempC:.2f}°C."

# API to convert Celcius to Fahrenheit New Comment
@flaskapp.route("/convertF/<tempC>")
def convertF(tempC):
    try:
        tempF = 9/5*(float(tempC))+32
#        logging.info(f"[INFO] Converted {tempC}°F to {tempF:.2f}°C.")
        return f"{tempC}°C is {tempF:.2f}°F."
#    except:
#        logging.warning("[WARN] Invalid temperature!")
