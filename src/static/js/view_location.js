let this_location = {};

function to_inventory() {
    window.location.href = url_base + '/website/inventory.html';
}

function to_locations() {
    window.location.href = 'http://127.0.0.1:5000/website/locations.html';
}

async function restart() {
    logout().then(_ => window.location.href = 'http://127.0.0.1:5000/website/user_login.html');
}

function to_settings() {
    window.location.href = 'http://127.0.0.1:5000/website/settings.html';
}

async function to_item(item) {
    await localStorage.setItem("item_to_show", JSON.stringify(item));
    window.location.href = url_base + '/website/view_item.html';
}

async function add_an_item_start() {
    add_item(this_location.uuid).then(_ => loader());
    await loader();
}

async function loader() {
    let location = JSON.parse(localStorage.getItem("location_to_show"));
    this_location = location;
    let pre = document.getElementById("location");
    pre.innerHTML = JSON.stringify(location, null, 2);
    let incoming_items = await get_location_items(location.uuid, 0);
    let inventory_items = await get_location_items(location.uuid, 1);
    let outgoing_items = await get_location_items(location.uuid, 2);
    let incoming_div = document.getElementById("incoming");
    incoming_div.innerHTML = "";
    incoming_div.appendChild(document.createElement("hr"));
    let inventory_div = document.getElementById("inventory");
    inventory_div.innerHTML = "";
    inventory_div.appendChild(document.createElement("hr"));
    let outgoing_div = document.getElementById("outgoing");
    outgoing_div.innerHTML = "";
    outgoing_div.appendChild(document.createElement("hr"));
    incoming_items.forEach(function (item) {
        let pre = document.createElement("pre");
        pre.innerText = JSON.stringify(item, null, 2);
        incoming_div.appendChild(pre);
        let button = document.createElement("button");
        button.innerText = "view/edit item";
        button.addEventListener(
            "click",
            async function () {
                await to_item(item);
            },
            false);
        incoming_div.appendChild(button);
        incoming_div.appendChild(document.createElement("hr"));
        incoming_div.appendChild(document.createElement("br"));
    });
    inventory_items.forEach(function (item) {
        let pre = document.createElement("pre");
        pre.innerText = JSON.stringify(item, null, 2);
        inventory_div.appendChild(pre);
        let button = document.createElement("button");
        button.innerText = "view/edit item";
        button.addEventListener(
            "click",
            async function () {
                await to_item(item);
            },
            false);
        inventory_div.appendChild(button);
        inventory_div.appendChild(document.createElement("hr"));
        inventory_div.appendChild(document.createElement("br"));
    });
    outgoing_items.forEach(function (item) {
        let pre = document.createElement("pre");
        pre.innerText = JSON.stringify(item, null, 2);
        outgoing_div.appendChild(pre);
        let button = document.createElement("button");
        button.innerText = "view/edit item";
        button.addEventListener(
            "click",
            async function () {
                await to_item(item);
            },
            false);
        outgoing_div.appendChild(button);
        outgoing_div.appendChild(document.createElement("hr"));
        outgoing_div.appendChild(document.createElement("br"));
    });
}

async function delete_location() {
    drop_location(this_location.uuid).then(_ => window.location.href = url_base + "/website/locations.html")
}

window.onload = loader;