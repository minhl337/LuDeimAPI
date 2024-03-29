import random
import json
import sys
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
	if "--local" not in sys.argv:
		if "--unsecure" not in sys.argv:
			cert = sys.argv[1]
			key = sys.argv[2]
			context = (cert, key)
			app.run(debug=True, port=4200, host="0.0.0.0", ssl_context=context)
		else:
			app.run(debug=True, port=4200, host="0.0.0.0")
	else:
		app.run(debug=True, port=4200)
