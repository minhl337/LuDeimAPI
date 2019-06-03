import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as log
import utils.typing as t


# this is on by default, read the docs to learn how to turn it off
def add_ints(params, _id, conn, logger, config):
    # the entire method gets wrapped in a try except to ensure any uncaught errors return a JSON-RPC error object
    # rather than an http 5xx.
    try:
        # get the typized version of config
        schemes = t.typize_config(config)
        # does the params object match any of your the param schemes specified in config.json ?
        if not t.check_params_against_scheme_set(schemes["add_ints"], params):
            # if not then throw a JSON-RPC error
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
        # do our calculation
        _sum = 0
        for i in params.values():
            _sum += i
        # lets log to stdout saying what we're doing (assuming debugging is on)
        logger.info("We just calculated the sum, {}. Now time to format and return the response!".format(_sum))
        # make and return our JSON-RPC response object
        return rpc.make_success_resp(_sum, _id)
    # catch everything!
    except Exception as e:
        # something went really wrong to be here. So, we write an error object to error.log for later review
        log.log_error({
            "method": "add_ints",
            "params": params,
            "error": str(e)
        })
        # finally, we return a JSON-RPC error saying something we messed up. Sorry 😢
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)