import utils.response_constants as const


def validate_request(request):
    try:
        req = request.get_json(force=True)
        return True
    except Exception as e:
        print(e)
        return make_error_resp(const.PARSE_ERR_CODE, const.PARSE_ERR, None)


def validate_batch(obj):
    if len(obj) == 0:
        return make_error_resp(const.INVALID_REQ_CODE, const.INVALID_REQ, None)
    else:
        return True


def validate_obj(obj, config):
    if not isinstance(obj, dict):
        return make_error_resp(const.PARSE_ERR_CODE, const.PARSE_ERR, None)
    if "id" not in obj:
        _id = None
    else:
        _id = obj["id"]
        if not (isinstance(_id, int) or isinstance(_id, str) or _id is None):
            return make_error_resp(const.INVALID_REQ_CODE, const.INVALID_REQ, None)
    if "jsonrpc" not in obj or "2.0" != obj["jsonrpc"]:
        return make_error_resp(const.INVALID_REQ_CODE, const.INVALID_REQ, None)
    if "method" not in obj:
        return make_error_resp(const.INVALID_REQ_CODE, const.INVALID_REQ, None)
    if obj["method"] not in config["method_names"]:
        return make_error_resp(const.NO_METHOD_CODE, const.NO_METHOD, _id)
    return True


def make_success_resp(result, _id):
    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": _id
    }


def make_error_resp(code, msg, _id):
    return {
        "jsonrpc": "2.0",
        "error": {
            "code": code,
            "message": msg
        },
        "id": _id
    }