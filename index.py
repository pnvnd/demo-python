from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.jinja2 import Jinja2Instrumentor

from flask import Flask, render_template
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
def hello_world():
    return render_template('hello.html')
