import logging

from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "root"

@app.route("/<authstuff>")
def root_with_stuff():
    logging.info(authstuff)
    return "ok"

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=5000, debug=True)
