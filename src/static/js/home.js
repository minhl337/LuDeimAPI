function load_inventory() {
    console.log("loading inventory");
    let request = make_request("get_inventory");
    console.log(request);
    // send request here
    let result = dummy_inventory_call_result;
    if (result.hasOwnProperty("result")) {
        let container = document.getElementById("inventory_lines");
        let outer_container = document.getElementById("inventory");
        let counter = 0;
        result = result["result"];
        result.forEach(function(e) {
            counter += 1;
            let el_div = document.createElement("div");
            el_div.innerText = e.main_info;
            el_div.style.lineHeight = "150%";
            el_div.style.backgroundColor = "black";
            if (e.incoming) {
                counter += 1;
                let incoming_tag = document.createElement("h6");
                incoming_tag.innerText = "INCOMING";
                incoming_tag.style.backgroundColor = "green";
                el_div.appendChild(incoming_tag);
                incoming_tag.style.margin = "0";
                incoming_tag.style.paddingLeft = "1vh";
            }
            if (e.outgoing) {
                counter += 1;
                let outgoing_tag = document.createElement("h6");
                outgoing_tag.innerText = "OUTGOING";
                outgoing_tag.style.backgroundColor = "blue";
                el_div.appendChild(outgoing_tag);
                outgoing_tag.style.margin = "0";
                outgoing_tag.style.paddingLeft = "1vh";
            }
            if (counter < 9) {
                container.appendChild(el_div);
                el_div.style.marginTop = "5px";
                el_div.style.marginBottom = "5px";
                el_div.style.padding = "5px";
            }
        });
        let see_all = document.createElement("button");
        see_all.innerText = "See All Inventory";
        outer_container.appendChild(see_all);
    } else if (result.hasOwnProperty("error")) {
        alert("The following error occurred while trying to load your inventory: " + result["error"]);
    } else {
        alert("An unknown issue occurred while trying to load your inventory.");
    }
}

function load_locations() {
    console.log("loading locations");
    let request = make_request("get_locations");
    console.log(request);
    // send request here
    let result = dummy_locations_call_result;
    if (result.hasOwnProperty("result")) {
        let container = document.getElementById("location_lines");
        let outer_container = document.getElementById("locations");
        let counter = 0;
        result = result["result"];
        let idx = 1;
        result.forEach(function(e) {
            counter += 1;
            let el_div = document.createElement("div");
            el_div.innerText = e.name;
            el_div.style.lineHeight = "150%";
            el_div.style.backgroundImage = "url(" + e.image + ")";
            if (counter < 6) {
                container.appendChild(el_div);
                el_div.style.marginTop = "5px";
                el_div.style.marginBottom = "5px";
                el_div.style.gridColumnStart = idx.toString();
                el_div.style.gridRowStart = "0";
                el_div.style.borderWidth = "thin";
                idx += 2;
            }
        });
        let see_all = document.createElement("button");
        see_all.innerText = "See All Locations";
        outer_container.appendChild(see_all);
    } else if (result.hasOwnProperty("error")) {
        alert("The following error occurred while trying to load your inventory: " + result["error"]);
    } else {
        alert("An unknown issue occurred while trying to load your inventory.");
    }
}

window.onload = function () {
    load_inventory();
    load_locations();
};