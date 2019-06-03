import concurrent
import sqlite3
import utils.response_constants as const
import utils.jsonrpc2 as rpc
import json
import application_handlers.handlers_consolidated as hc


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
        executor = concurrent.ThreadPoolExecutor(max_workers=(len(obj) % 20))
        promises = []
        for _ in obj:
            promises.append(executor.submit(handle_obj, _, config, logger, session))
        results = []
        for promise in promises:
            result = promise.result()
            if result != const.NO_RESPONSE:
                results.append(result)
        if len(results) == 0:
            results = const.NO_RESPONSE
        return results
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
    return methods.get(
        method_name,
        lambda v, w, x, y, z: rpc.make_error_resp(const.NO_METHOD_CODE, const.NO_METHOD, _id)
    )(params, _id, conn, logger, config, session)
