function build_header() {
    let body = document.getElementsByTagName("body")[0];
    let header_text = document.createElement("div");
    header_text.innerText = "Home";
    header_text.style.display = "grid";
    header_text.style.gridColumnStart = "2";
    header_text.style.gridColumnEnd = "150";
    header_text.style.gridRowStart = "2";
    header_text.style.gridRowEnd = "17";
    header_text.style.margin = "0";
    header_text.style.fontSize = "14vh";
    header_text.style.fontFamily = "sans-serif";
    body.appendChild(header_text);
    let name = document.createElement("div");
    name.innerText = "example username";
    name.style.gridColumnStart = "150";
    name.style.gridColumnEnd = "200";
    name.style.gridRowStart = "2";
    name.style.gridRowEnd = "9";
    name.style.fontSize = "100%";
    name.style.margin = "0";
    name.style.fontFamily = "sans-serif";
    name.style.textAlign = "right";
    body.appendChild(name);
    let signout_icon = document.createElement("div");
    signout_icon.className = "fas fa-sign-out-alt";
    signout_icon.style.gridColumnStart = "195";
    signout_icon.style.gridColumnEnd = "200";
    signout_icon.style.gridRowStart = "9";
    signout_icon.style.gridRowEnd = "17";
    signout_icon.style.fontSize = "2em";
    signout_icon.style.margin = "auto";
    signout_icon.onclick = logout;
    body.appendChild(signout_icon);
    let settings_icon = document.createElement("div");
    settings_icon.className = "fas fa-cogs";
    settings_icon.style.gridColumnStart = "189";
    settings_icon.style.gridColumnEnd = "194";
    settings_icon.style.gridRowStart = "9";
    settings_icon.style.gridRowEnd = "17";
    settings_icon.style.fontSize = "2em";
    settings_icon.style.margin = "auto";
    body.appendChild(settings_icon);
    let header_break = document.createElement("hr");
    header_break.style.gridRowStart = "17";
    header_break.style.gridRowEnd = "19";
    header_break.style.gridColumnStart = "2";
    header_break.style.gridColumnEnd = "200";
    header_break.size = 5;
    header_break.style.margin = "0";
    header_break.style.backgroundColor = "black";
    header_break.style.border = "none";
    header_break.noShade = true;
    body.appendChild(header_break);
}

function build_inventory() {
    console.log("loading inventory");
    // send request here
    let result = dummy_inventory_call_result;
    if (result.hasOwnProperty("result")) {
        let row_start = 25;
        let body = document.getElementsByTagName("body")[0];
        let title = document.createElement("div");
        title.style.gridColumnStart = "2";
        title.style.gridColumnEnd = "200";
        title.style.gridRowStart = "20";
        title.style.gridRowEnd = "24";
        title.innerText = "Inventory";
        title.style.fontFamily = "sans-serif";
        body.appendChild(title);
        result = result["result"];
        result.forEach(function(e) {
            let end_col = 200;
            let el_div = document.createElement("div");
            el_div.innerText = e.main_info;
            el_div.style.color = "white";
            el_div.style.backgroundColor = "black";
            el_div.style.gridColumnStart = "2";
            el_div.style.gridRowStart = row_start.toString();
            el_div.style.gridRowEnd = (row_start + 4).toString();
            if (e.incoming) {
                let incoming_tag = document.createElement("div");
                incoming_tag.innerText = "INCOMING";
                incoming_tag.style.backgroundColor = "green";
                if (row_start < 55) {
                    body.appendChild(incoming_tag);
                }
                incoming_tag.style.margin = "0";
                incoming_tag.style.width = "100%";
                incoming_tag.style.height = "100%";
                incoming_tag.style.gridRowStart = row_start.toString();
                incoming_tag.style.gridRowEnd = (row_start + 4).toString();
                incoming_tag.style.gridColumnEnd = end_col.toString();
                incoming_tag.style.gridColumnStart = (end_col - 20).toString();
                end_col -= 21;
            }
            if (e.outgoing) {
                let outgoing_tag = document.createElement("div");
                outgoing_tag.innerText = "OUTGOING";
                outgoing_tag.style.backgroundColor = "blue";
                if (row_start < 55) {
                    body.appendChild(outgoing_tag);
                }
                outgoing_tag.style.margin = "0";
                outgoing_tag.style.width = "100%";
                outgoing_tag.style.height = "100%";
                outgoing_tag.style.gridRowStart = row_start.toString();
                outgoing_tag.style.gridRowEnd = (row_start + 4).toString();
                outgoing_tag.style.gridColumnEnd = end_col.toString();
                outgoing_tag.style.gridColumnStart = (end_col - 20).toString();
                end_col -= 21;
            }
            if (row_start < 55) {
                body.appendChild(el_div);
                el_div.style.gridColumnEnd = end_col.toString();
            }
            row_start += 5;
        });
        let see_all = document.createElement("button");
        see_all.innerText = "See All Inventory";

    } else if (result.hasOwnProperty("error")) {
        alert("The following error occurred while trying to load your inventory: " + result["error"]);
    } else {
        alert("An unknown issue occurred while trying to load your inventory.");
    }
}

function logout() {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/cache/clear", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send("");
    window.location.href = 'http://127.0.0.1:5000/login/';
}

window.onload = function () {
    build_header();
    build_inventory();
};