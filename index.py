import newrelic.agent
newrelic.agent.initialize()

from opentelemetry.instrumentation.flask import FlaskInstrumentor

from flask import Flask
app = Flask(__name__)

import uuid
serviceId = str(uuid.uuid1())

FlaskInstrumentor().instrument_app(app)

@app.route('/')
def hello_world():
    return 'Hello World!'
