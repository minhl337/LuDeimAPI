let url_base = "http://165.22.206.32:4200";

async function req(method_name, params, id) {
    let url = url_base + "/api/";
    let payload = {
        "jsonrpc": "2.0",
        "method": method_name,
        "params": params,
        "id": id
    };
    let response = await fetch(
        url,
        {
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, cors, *same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {'Content-Type': 'application/json'},
            redirect: 'follow', // manual, *follow, error
            referrer: 'no-referrer', // no-referrer, *client
            body: JSON.stringify(payload), // body data type must match "Content-Type" header
        }
    );
    if (!response.ok) throw "the server returned a hard error violating the json-rpc 2.0 standard.";
    response = await response.json();
    if (await response.hasOwnProperty("error")) {
        alert(JSON.stringify(await response["error"]));
        throw JSON.stringify(await response["error"]);
    }
    return await response["result"];
}

async function login_user(username, password_hash) {
    return await req(
        "login_user",
        {
            "username": username,
            "password_hash": password_hash
        },
        1
    );
}

async function logout() {
    return await req(
        "logout",
        {},
        1
    )
}

async function add_location(type, name, address, latitude, longitude, details, representative) {
    return await req(
        "add_location",
        {
            "type": type,
            "name": name,
            "address": address,
            "latitude": latitude,
            "longitude": longitude,
            "details": details,
            "representative": representative
        },
        1
    )
}

async function change_username(new_username) {
    return await req(
        "change_username",
        {
            "new_username": new_username
        },
        1
    )
}

async function change_password_hash(new_password_hash) {
    return await req(
        "change_password_hash",
        {
            "new_password_hash": new_password_hash
        },
        1
    )
}

async function change_avatar(new_avatar) {
    return await req(
        "change_avatar",
        {
            "new_avatar": new_avatar
        },
        1
    )
}

async function get_user_items(stage_filter = null) {
    if (stage_filter !== null) {
        return await req(
            "get_user_items",
            {
                "stage_filter": stage_filter
            },
            1
        )
    } else {
        return await req(
            "get_user_items",
            {},
            1
        )
    }
}

async function add_item(location_uuid, type = "diamond") {
    return req(
        "add_item",
        {
            "location_uuid": location_uuid,
            "type": type
        },
        1
    )
}

async function get_location_items(location_uuid, stage_filter = null) {
    if (stage_filter !== null) {
        return await req(
            "get_location_items",
            {
                "uuid": location_uuid,
                "stage_filter": stage_filter
            },
            1
        )
    } else {
        return await req(
            "get_location_items",
            {
                "uuid": location_uuid
            },
            1
        )
    }
}

async function drop_item(item_uuid) {
    return await req(
        "drop_item",
        {
            "item_uuid": item_uuid,
        },
        1
    )
}

async function drop_location(location_uuid) {
    return await req(
        "drop_location",
        {"location_uuid": location_uuid},
        1
    )
}

async function begin_transfer(item_uuid, dest_user_uuid, dest_location_uuid) {
    return await req(
        "begin_transfer",
        {
            "item_uuid": item_uuid,
            "destination_location_uuid": dest_location_uuid,
            "destination_user_uuid": dest_user_uuid
        },
        1
    )
}

async function get_all_users() {
    return await req(
        "get_all_users",
        {},
        1
    )
}

async function get_user_locations(username = null) {
    if (username !== null) {
        return await req(
            "get_user_locations",
            {
                "username": username
            },
            1
        )
    } else {
        return await req(
            "get_user_locations",
            {},
            1
        )
    }
}

async function get_sess() {
    return await req("get_sess", {}, 1);
}

async function accept_transfer(item_uuid) {
    return await req(
        "accept_transfer",
        {
            "item_uuid": item_uuid
        },
        1
    )
}

async function reject_transfer(item_uuid) {
    return await req(
        "reject_transfer",
        {
            "item_uuid": item_uuid
        },
        1
    )
}

async function rescind_transfer(item_uuid) {
    return await req(
        "rescind_transfer",
        {
            "item_uuid": item_uuid
        },
        1
    )
}

async function redirect_transfer(item_uuid, new_dest_user_uuid, new_dest_location_uuid) {
    return await req(
        "redirect_transfer",
        {
            "item_uuid": item_uuid,
            "new_destination_location_uuid": new_dest_location_uuid,
            "new_destination_user_uuid": new_dest_user_uuid
        },
        1
    )
}

async function split_item(item_uuid, ways=null) {
    if (ways !== null) {
        return await req(
            "split_item",
            {
                "item_uuid": item_uuid,
                "ways": ways
            },
            1
        )
    } else {
        return await req(
            "split_item",
            {
                "item_uuid": item_uuid,
            },
            1
        )
    }
}

async function change_item_detail(item_uuid, key, value) {
    return await req(
            "change_item_detail",
            {
                "item_uuid": item_uuid,
                "key": key,
                "value": value
            },
            1
        )
}