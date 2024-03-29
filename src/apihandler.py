import concurrent.futures
import sqlite3
import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.typing as t
import json
import application_handlers.handlers_consolidated as hc
from flask import jsonify


methods = dict()
for method_name in json.load(open("config.json", "r"))["method_names"]:
    methods[method_name] = getattr(hc, method_name)


def handle_request(request, logger, session):
    evaluation = rpc.validate_request(request)
    if evaluation is True:
        req = request.get_json(force=True)
        if isinstance(req, list):
            return handle_batch(req, logger, session)
        else:
            config = json.load(open("config.json", "r"))
            return handle_obj(req, config, logger, session)
    else:
        return evaluation


def handle_batch(obj, logger, session):
    evaluation = rpc.validate_batch(obj)
    if evaluation is True:
        config = json.load(open("config.json", "r"))
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=(len(obj) % 20))
        promises = []
        sessions = []
        for _ in obj:
            d_sess = dictize_session(session)
            sessions.append(d_sess)
            promises.append(executor.submit(handle_obj, _, config, logger, d_sess))
        results = []
        for promise in promises:
            result = promise.result()
            if result != const.NO_RESPONSE:
                results.append(result)
        for d_sess in sessions:
            for k in d_sess:
                session[k] = d_sess[k]
        if len(results) == 0:
            return const.NO_RESPONSE
        resp = jsonify(results)
        resp.headers.add("Access-Control-Allow-Headers",
                         "Origin, X-Requested-With, Content-Type, Accept, x-auth")
        return resp
    else:
        return evaluation


def handle_obj(obj, config, logger, session):
    evaluation = rpc.validate_obj(obj, config)
    if evaluation is True:
        method_name = obj["method"]
        params = obj.get("params", {})
        _id = obj.get("id", None)
        conn = sqlite3.connect(config["database_path"], isolation_level="EXCLUSIVE")
        result = method_call(method_name, params, _id, conn, logger, config, session)
        conn.close()
        if "id" in obj:
            return result
        else:
            return const.NO_RESPONSE
    else:
        return evaluation


def method_call(method_name, params, _id, conn, logger, config, session):
    logger.info("[calling] {} with {}".format(method_name, params))
    schemes = t.typize_config(config)
    if not t.check_params_against_scheme_set(schemes.get(method_name, None), params):
        return rpc.make_error_resp(const.INVALID_PARAMS_CODE, const.INVALID_PARAMS, _id)
    return methods.get(
        method_name,
        lambda v, w, x, y, z: rpc.make_error_resp(const.NO_METHOD_CODE, const.NO_METHOD, _id)
    )(params, _id, conn, logger, config, session)


def dictize_session(s):
    d = dict()
    for k in s:
        d[k] = s[k]
    return d

