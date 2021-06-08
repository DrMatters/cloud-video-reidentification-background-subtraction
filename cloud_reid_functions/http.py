from flask import request, Flask
from event_collector.main import event_collector
from event_handler.main import event_handler

app = Flask(__name__)


@app.route('/event_handler', methods=['GET', 'POST', 'HEAD', 'OPTIONS'])
def event_handler_wrapper():
    return event_handler(request)


@app.route('/event_collector', methods=['GET', 'POST', 'HEAD', 'OPTIONS'])
def event_collector_wrapper():
    return event_collector(request)


if __name__ == '__main__':
    app.run()
