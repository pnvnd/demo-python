import newrelic.agent
newrelic.agent.initialize()

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from flask import Flask
app = Flask(__name__)

import uuid
serviceId = str(uuid.uuid1())

trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "demo-flask.otel", "service.instance.id": serviceId, "tag.team": "datacrunch-prod"})))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

FlaskInstrumentor().instrument_app(app)

@app.route('/')
def hello_world():
    return 'Hello World!'
