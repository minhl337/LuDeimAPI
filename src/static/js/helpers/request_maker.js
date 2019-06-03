function make_request(params, method) {
    return {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
}