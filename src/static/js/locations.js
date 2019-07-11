function to_inventory() {
    window.location.href = url_base + '/website/inventory.html';
}

async function restart() {
    logout().then(_ => window.location.href = url_base + '/website/user_login.html');
}

function to_settings() {
    window.location.href = url_base + '/website/settings.html';
}

async function load_locations() {
    let locations = await get_user_locations();
    let locations_div = document.getElementById("locations");
    locations_div.innerHTML = "";
    locations.forEach(function (location) {
        let pre = document.createElement("pre");
        pre.innerText = JSON.stringify(location, null, 2);
        locations_div.appendChild(pre);
        let button = document.createElement("button");
        button.innerText = "view/edit location";
        button.addEventListener(
            "click",
            async function () {
                await to_location(location);
            },
            false);
        locations_div.appendChild(button);
        locations_div.appendChild(document.createElement("hr"));
        locations_div.appendChild(document.createElement("br"));
    });
}

async function to_location(location) {
    await localStorage.setItem("location_to_show", JSON.stringify(location));
    window.location.href = url_base + '/website/view_location.html';
}

async function add_a_location_start() {
    let target = document.getElementById("add_a_location");
    let cont_div = document.createElement("div");
    cont_div.id = "add_a_location";
    cont_div.appendChild(document.createElement("hr"));
    cont_div.appendChild(document.createElement("br"));

    let type_select_label = document.createElement("label");
    type_select_label.innerText = "Location Type: ";
    cont_div.appendChild(type_select_label);

    let type_select = document.createElement("select");
    type_select.id = "type_select";
    let opt1 = document.createElement("option");
    opt1.value = "mine";
    opt1.innerText = "Mine";
    type_select.add(opt1);
    let opt2 = document.createElement("option");
    opt2.value = "warehouse";
    opt2.innerText = "Warehouse";
    type_select.add(opt2);
    let opt3 = document.createElement("option");
    opt3.value = "store";
    opt3.innerText = "Store";
    type_select.add(opt3);
    cont_div.appendChild(type_select);

    cont_div.appendChild(document.createElement("br"));

    let name_label = document.createElement("label");
    name_label.innerText = "Location Name: ";
    cont_div.appendChild(name_label);

    let name_textbox = document.createElement("input");
    name_textbox.type = "text";
    name_textbox.id = "name_textbox";
    cont_div.appendChild(name_textbox);

    cont_div.appendChild(document.createElement("br"));

    let address_label = document.createElement("label");
    address_label.innerText = "Location Address: ";
    cont_div.appendChild(address_label);

    let address_textbox = document.createElement("input");
    address_textbox.type = "text";
    address_textbox.id = "address_textbox";
    cont_div.appendChild(address_textbox);

    cont_div.appendChild(document.createElement("br"));

    let latitude_label = document.createElement("label");
    latitude_label.innerText = "Location Latitude (decimal): ";
    cont_div.appendChild(latitude_label);

    let latitude_textbox = document.createElement("input");
    latitude_textbox.type = "number";
    latitude_textbox.id = "latitude_textbox";
    cont_div.appendChild(latitude_textbox);

    cont_div.appendChild(document.createElement("br"));

    let longitude_label = document.createElement("label");
    longitude_label.innerText = "Location Longitude (decimal): ";
    cont_div.appendChild(longitude_label);

    let longitude_textbox = document.createElement("input");
    longitude_textbox.type = "number";
    longitude_textbox.id = "longitude_textbox";
    cont_div.appendChild(longitude_textbox);

    cont_div.appendChild(document.createElement("br"));

    let rep_title_label = document.createElement("label");
    rep_title_label.innerText = "Location Representative Title: ";
    cont_div.appendChild(rep_title_label);

    let rep_title_select = document.createElement("select");
    rep_title_select.id = "rep_title_select";
    let topt1 = document.createElement("option");
    topt1.value = "MR";
    topt1.innerText = "Mr";
    rep_title_select.add(topt1);
    let topt2 = document.createElement("option");
    topt2.value = "MRS";
    topt2.innerText = "Mrs";
    rep_title_select.add(topt2);
    let topt3 = document.createElement("option");
    topt3.value = "MISS";
    topt3.innerText = "Miss";
    rep_title_select.add(topt3);
    let topt4 = document.createElement("option");
    topt4.value = "DR";
    topt4.innerText = "Dr";
    rep_title_select.add(topt4);
    cont_div.appendChild(rep_title_select);

    cont_div.appendChild(document.createElement("br"));

    let rep_first_name_label = document.createElement("label");
    rep_first_name_label.innerText = "Location Representative First Name: ";
    cont_div.appendChild(rep_first_name_label);

    let rep_first_name_textbox = document.createElement("input");
    rep_first_name_textbox.type = "text";
    rep_first_name_textbox.id = "rep_first_name_textbox";
    cont_div.appendChild(rep_first_name_textbox);

    cont_div.appendChild(document.createElement("br"));

    let rep_last_name_label = document.createElement("label");
    rep_last_name_label.innerText = "Location Representative Last Name: ";
    cont_div.appendChild(rep_last_name_label);

    let rep_last_name_textbox = document.createElement("input");
    rep_last_name_textbox.type = "text";
    rep_last_name_textbox.id = "rep_last_name_textbox";
    cont_div.appendChild(rep_last_name_textbox);

    cont_div.appendChild(document.createElement("br"));

    let rep_contact_label = document.createElement("label");
    rep_contact_label.innerText = "Location Representative Contact Info: ";
    cont_div.appendChild(rep_contact_label);

    let rep_contact_textbox = document.createElement("input");
    rep_contact_textbox.type = "text";
    rep_contact_textbox.id = "rep_contact_textbox";
    cont_div.appendChild(rep_contact_textbox);

    cont_div.appendChild(document.createElement("br"));

    let submit_button = document.createElement("button");
    submit_button.innerHTML = "Submit";
    submit_button.addEventListener(
            "click",
            add_a_location_submit,
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
    let target = document.getElementById("add_a_location");
    let b = document.createElement("input");
    b.id = "add_a_location";
    b.type = "submit";
    b.value = "Add Location";
    b.addEventListener(
            "click",
            add_a_location_start,
            false
    );
    target.replaceWith(b);
}

async function add_a_location_submit() {
    let type = document.getElementById("type_select").value;
    let name = document.getElementById("name_textbox").value;
    let address = document.getElementById("address_textbox").value;
    let latitude = parseFloat(document.getElementById("latitude_textbox").value);
    let longitude = parseFloat(document.getElementById("longitude_textbox").value);
    let details = "";
    let title = document.getElementById("rep_title_select").value;
    let rep_first_name = document.getElementById("rep_first_name_textbox").value;
    let rep_last_name = document.getElementById("rep_last_name_textbox").value;
    let contact_info = document.getElementById("rep_contact_textbox").value;
    let representative = {
        "title": title,
        "first_name": rep_first_name,
        "last_name": rep_last_name,
        "contact_info": contact_info
    };
    add_location(type, name, address, latitude, longitude, details, representative)
        .then(_ => load_locations());
    await back_to_normal()
}

window.onload = async function() {
    await load_locations();
};