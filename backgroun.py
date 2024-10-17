from threading import Thread

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'I am alive'


def run():
    app.run(host='0.0.0.0', port=80)


def keep_alive():
    t = Thread(target=run)
    t.start()
