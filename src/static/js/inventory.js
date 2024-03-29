let locations = [];

function to_inventory() {
    window.location.href = url_base + '/website/inventory.html';
}

function to_locations() {
    window.location.href = url_base + '/website/locations.html';
}

async function restart() {
    logout().then(_ => window.location.href = url_base + '/website/user_login.html');
}

function to_settings() {
    window.location.href = url_base + '/website/settings.html';
}

async function to_item(item) {
    await localStorage.setItem("item_to_show", JSON.stringify(item));
    window.location.href = url_base + '/website/view_item.html';
}

async function add_an_item_start() {
    let target = document.getElementById("add_an_item");
    let cont_div = document.createElement("div");
    cont_div.id = "add_an_item";
    cont_div.appendChild(document.createElement("hr"));
    cont_div.appendChild(document.createElement("br"));

    let type_select_label = document.createElement("label");
    type_select_label.innerText = "Location to add item to: ";
    cont_div.appendChild(type_select_label);

    let selection = document.createElement("select");
    selection.id = "selection_id";
    locations.forEach(function (location) {
        let opt = document.createElement("option");
        opt.value = location.uuid;
        opt.innerText = location.name;
        selection.add(opt);
    });
    cont_div.appendChild(selection);

    cont_div.appendChild(document.createElement("br"));

    let submit_button = document.createElement("button");
    submit_button.innerHTML = "Submit";
    submit_button.addEventListener(
            "click",
            add_an_item_submit,
            false
    );
    cont_div.appendChild(submit_button);

    let cancel_button = document.createElement("button");
    cancel_button.innerHTML = "Cancel";
    cancel_button.addEventListener(
            "click",
            back_to_normal,
            false
    );
    cont_div.appendChild(cancel_button);

    target.replaceWith(cont_div);
}

async function back_to_normal() {
    let target = document.getElementById("add_an_item");
    let b = document.createElement("input");
    b.id = "add_an_item";
    b.type = "submit";
    b.value = "Add Item";
    b.addEventListener(
            "click",
            add_an_item_start,
            false
    );
    target.replaceWith(b);
}

async function add_an_item_submit() {
    let location_uuid = document.getElementById("selection_id").value;
    add_item(location_uuid).then(_ => loader());
    await back_to_normal()
}

async function load_locations() {
    (await get_user_locations()).forEach(function(l) {
        locations.push(l);
    });
}

async function loader() {
    let incoming_items = await get_user_items(0);
    let inventory_items = await get_user_items(1);
    let outgoing_items = await get_user_items(2);
    let incoming_div = document.getElementById("incoming");
    incoming_div.innerHTML = "";
    let inventory_div = document.getElementById("inventory");
    inventory_div.innerHTML = "";
    let outgoing_div = document.getElementById("outgoing");
    outgoing_div.innerHTML = "";
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


window.onload = async function () {
    await load_locations();
    await loader();
};