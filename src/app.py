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
        return json.dumps(resp)


# # cache
# @app.route("/cache/get")
# def get_cache():
#     r = dict()
#     for k in session.keys():
#         r[k] = session[k]
#     return json.dumps(r)
#
#
# @app.route("/cache/put", methods=["POST"])
# def put_cache():
#     j = request.get_json()
#     for key in j:
#         session[key] = j[key]
#     return ""
#
#
# @app.route("/cache/clear", methods=["POST", "GET"])
# def clear_cache():
#     session.clear()
#     return ""
#
#
# # pages
# @app.route("/login/")
# def login():
#     if "user_id" in session:
#         return redirect(url_for("home"))
#     return render_template("login.html")
#
#
# @app.route("/home/")
# def home():
#     return render_template("home.html")
#
#
# @app.route("/home_grid/")
# def home_grid():
#     return render_template("home_grid.html")


if __name__ == "__main__":
    app.secret_key = "AmySantiago"
    app.run(debug=True)
