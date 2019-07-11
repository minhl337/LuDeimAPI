import random
import json
import apihandler as handle
import utils.response_constants as const
from flask import Flask, request, render_template, session, redirect, url_for


app = Flask(__name__)


@app.route("/")
def hello_world():
    continuity_int = random.randint(-1000, 1000)
    app.logger.info("Continuity int: {}".format(continuity_int))
    return "Server Working. Continuity int: {}".format(continuity_int)


@app.route("/api/", methods=["POST"])
def api_endpoint():
    resp = handle.handle_request(request, app.logger, session)
    if resp != const.NO_RESPONSE:
        return resp


@app.route("/website/<path:path>")
def website(path):
    return render_template(path)


if __name__ == "__main__":
    app.secret_key = "AmySantiago"
    app.run(debug=True, port=4200)
