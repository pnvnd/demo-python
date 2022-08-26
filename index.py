import newrelic.agent
newrelic.agent.initialize()

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
