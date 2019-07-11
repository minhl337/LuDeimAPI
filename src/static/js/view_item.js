let this_item = {};
let users = [];
let selected_user = null;
let ways = 2;

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

async function set_clarity() {
    let clarity = document.getElementById("clarity").value;
    await change_item_detail(this_item.uuid, "clarity", clarity);
    await dynamic_reload();
}

async function set_color() {
    let color = document.getElementById("color").value;
    await change_item_detail(this_item.uuid, "color", color);
    await dynamic_reload();
}

async function set_cut() {
    let cut = document.getElementById("cut").value;
    await change_item_detail(this_item.uuid, "cut", cut);
    await dynamic_reload();
}

async function set_carat() {
    let carat = document.getElementById("carat").value;
    await change_item_detail(this_item.uuid, "carat", carat);
    await dynamic_reload();
}

async function set_usd_price() {
    let usd_price = document.getElementById("usd_price").value;
    await change_item_detail(this_item.uuid, "usd_price", usd_price);
    await dynamic_reload();
}

async function set_dob() {
    let dob = document.getElementById("dob").value;
    await change_item_detail(this_item.uuid, "dob", dob);
    await dynamic_reload();
}

async function set_tender_house() {
    let tender_house = document.getElementById("tender_house").value;
    await change_item_detail(this_item.uuid, "tender_house", tender_house);
    await dynamic_reload();
}

async function set_tender_date() {
    let tender_date = document.getElementById("tender_date").value;
    await change_item_detail(this_item.uuid, "tender_date", tender_date);
    await dynamic_reload();
}

async function set_tender_house_exchange_rate() {
    let tender_house_exchange_rate = document.getElementById("tender_house_exchange_rate").value;
    await change_item_detail(this_item.uuid, "tender_house_exchange_rate", tender_house_exchange_rate);
    await dynamic_reload();
}

async function set_cut_date() {
    let cut_date = document.getElementById("cut_date").value;
    await change_item_detail(this_item.uuid, "cut_date", cut_date);
    await dynamic_reload();
}

async function set_gia() {
    let gia = document.getElementById("gia").value;
    await change_item_detail(this_item.uuid, "gia", gia);
    await dynamic_reload();
}

async function set_jewelery_description() {
    let jewelery_description = document.getElementById("jewelery_description").value;
    await change_item_detail(this_item.uuid, "jewelery_description", jewelery_description);
    await dynamic_reload();
}

async function set_jewelery_number() {
    let jewelery_number = document.getElementById("jewelery_number").value;
    await change_item_detail(this_item.uuid, "jewelery_number", jewelery_number);
    await dynamic_reload();
}

async function transfer_this_item_start() {
    let button2replace = document.getElementById("transfer_btn");
    let cont_div = document.createElement("div");
    cont_div.appendChild(document.createElement("hr"));
    cont_div.id = "transfer_btn";
    let cancel_button = document.createElement("button");
    cancel_button.innerHTML = "Cancel";
    cancel_button.addEventListener(
            "click",
            back_to_normal,
            false
    );
    cont_div.appendChild(cancel_button);
    cont_div.appendChild(document.createElement("br"));
    let label = document.createElement("label");
    label.id = "label";
    label.innerText = "Select The recipient user (select yourself for an internal transfer): ";
    cont_div.appendChild(label);
    users = await get_all_users();
    let selector = document.createElement("select");
    selector.id = "selector";
    users.forEach(function (user) {
        let opt = document.createElement("option");
        opt.value = user.username;
        opt.innerText = user.username;
        selector.add(opt);
    });
    cont_div.appendChild(selector);
    let continue_btn = document.createElement("input");
    continue_btn.addEventListener("click", transfer_this_item_stage2, false);
    continue_btn.innerHTML = "Continue";
    continue_btn.id = "cont_btn";
    continue_btn.type = "Submit";
    cont_div.appendChild(document.createElement("br"));
    cont_div.appendChild(continue_btn);
    cont_div.appendChild(document.createElement("hr"));
    button2replace.replaceWith(cont_div);
}

async function transfer_this_item_stage2() {
    document.getElementById("label").innerText = "Select The destination location: ";
    let selector = document.getElementById("selector");
    let username = selector.value;
    selector.innerHTML = "";
    users.forEach(function (u) {
        if (u.username === username) selected_user = u;
    });
    (await get_user_locations(username)).forEach(function (loc) {
        let opt = document.createElement("option");
        opt.value = loc.uuid;
        opt.innerText = loc.name;
        selector.add(opt);
    });
    let btn = document.getElementById("cont_btn");
    btn.removeEventListener("click", transfer_this_item_stage2);
    btn.addEventListener("click", transfer_this_item_submit, false);
    btn.innerHTML = "Submit";
}

async function transfer_this_item_submit() {
    await begin_transfer(this_item.uuid, selected_user.uuid, document.getElementById("selector").value);
    await back_to_normal();
}

async function drop_this_item() {
    await drop_item(this_item.uuid);
    window.location.href = url_base + '/website/inventory.html'
}

async function back_to_normal() {
    await dynamic_reload();
}

async function accept_this_item() {
    let resp = await accept_transfer(this_item.uuid);
    await dynamic_reload();
}

async function reject_this_item() {
    let resp = await reject_transfer(this_item.uuid);
    await dynamic_reload();
}

async function rescind_this_item() {
    let resp = await rescind_transfer(this_item.uuid);
    await dynamic_reload();
}

async function start_redirect() {
    let button2replace = document.getElementById("redirect_transfer_btn");
    let cont_div = document.createElement("div");
    cont_div.appendChild(document.createElement("hr"));
    cont_div.id = "redirect_transfer_btn";
    let cancel_button = document.createElement("button");
    cancel_button.innerHTML = "Cancel";
    cancel_button.addEventListener(
            "click",
            back_to_normal,
            false
    );
    cont_div.appendChild(cancel_button);
    cont_div.appendChild(document.createElement("br"));
    let label = document.createElement("label");
    label.id = "label";
    label.innerText = "Select The new recipient user: ";
    cont_div.appendChild(label);
    users = await get_all_users();
    let selector = document.createElement("select");
    selector.id = "selector";
    users.forEach(function (user) {
        let opt = document.createElement("option");
        opt.value = user.username;
        opt.innerText = user.username;
        selector.add(opt);
    });
    cont_div.appendChild(selector);
    let continue_btn = document.createElement("input");
    continue_btn.addEventListener("click", redirect_stage2, false);
    continue_btn.innerHTML = "Continue";
    continue_btn.id = "cont_btn";
    continue_btn.type = "Submit";
    cont_div.appendChild(document.createElement("br"));
    cont_div.appendChild(continue_btn);
    cont_div.appendChild(document.createElement("hr"));
    button2replace.replaceWith(cont_div);
}

async function redirect_stage2() {
    document.getElementById("label").innerText = "Select The new destination" +
        " location: ";
    let selector = document.getElementById("selector");
    let username = selector.value;
    selector.innerHTML = "";
    users.forEach(function (u) {
        if (u.username === username) selected_user = u;
    });
    (await get_user_locations(username)).forEach(function (loc) {
        let opt = document.createElement("option");
        opt.value = loc.uuid;
        opt.innerText = loc.name;
        selector.add(opt);
    });
    let btn = document.getElementById("cont_btn");
    btn.removeEventListener("click", redirect_stage2);
    btn.addEventListener("click", redirect_submit, false);
    btn.innerHTML = "Submit";
}

async function redirect_submit() {
    await redirect_transfer(this_item.uuid, selected_user.uuid, document.getElementById("selector").value);
    await back_to_normal();
}

async function start_split() {
    let button2replace = document.getElementById("split_btn");
    let cont_div = document.createElement("div");
    cont_div.appendChild(document.createElement("hr"));
    cont_div.id = "split_btn";
    let cancel_button = document.createElement("button");
    cancel_button.innerHTML = "Cancel";
    cancel_button.addEventListener(
            "click",
            dynamic_reload,
            false
    );
    cont_div.appendChild(cancel_button);
    cont_div.appendChild(document.createElement("br"));
    let label = document.createElement("label");
    label.id = "label";
    label.innerText = "How many items would you like to split this item into: ";
    cont_div.appendChild(label);
    let num = document.createElement("input");
    num.type = "number";
    num.id = "num";
    cont_div.appendChild(num);
    let continue_btn = document.createElement("input");
    continue_btn.addEventListener("click", split_stage2, false);
    continue_btn.innerHTML = "Continue";
    continue_btn.id = "cont_btn";
    continue_btn.type = "Submit";
    cont_div.appendChild(document.createElement("br"));
    cont_div.appendChild(continue_btn);
    cont_div.appendChild(document.createElement("hr"));
    button2replace.replaceWith(cont_div);
}

async function split_stage2() {
    let cont_div = document.getElementById("split_btn");
    ways = parseInt(document.getElementById("num").value);
    cont_div.innerHTML = "";
    cont_div.appendChild(document.createElement("hr"));
    cont_div.id = "split_btn";
    let cancel_button = document.createElement("button");
    cancel_button.innerHTML = "Cancel";
    cancel_button.addEventListener(
            "click",
            dynamic_reload,
            false
    );
    cont_div.appendChild(cancel_button);
    cont_div.appendChild(document.createElement("br"));
    for (let i = 0; i < ways; i++) {
        let label = document.createElement("label");
        label.innerText = "Item " + i.toString() + "'s Size (Carat): ";
        cont_div.appendChild(label);
        let tb = document.createElement("input");
        tb.type = "number";
        tb.id = "item_" + i.toString();
        tb.value = "0.0";
        cont_div.append(tb);
        cont_div.append(document.createElement("br"));
    }
    let file_upload = document.createElement("input");
    file_upload.type = "file";
    file_upload.id = "file_upload";
    file_upload.name = "file";
    cont_div.appendChild(file_upload);
    cont_div.append(document.createElement("br"));
    let btn = document.createElement("input");
    btn.id = "cont_btn";
    btn.type = "Submit";
    btn.addEventListener("click", split_submit, false);
    btn.innerHTML = "Submit";
    cont_div.appendChild(btn);
    cont_div.append(document.createElement("hr"));
}

async function split_submit() {
    let file_uploader = document.getElementById("file_upload");
    if (file_uploader.value === "" || file_uploader.files.length > 1) {
        alert("you must upload exactly one invoice");
    } else {
        console.log(file_uploader.files);
        let resp = await upload_file(file_uploader.files[0]);
        console.log(resp);
        await change_item_detail(
                this_item.uuid,
                "cutter_invoice",
                resp["filename"]
            );
        let resps = await split_item(this_item.uuid, ways);
        resps.forEach(async function (resp, i) {
            await change_item_detail(
                resp.uuid,
                "carat",
                document.getElementById("item_" + i.toString()).value
            )
        });
        window.location.href = url_base + '/website/inventory.html';
    }
}

async function dynamic_reload() {
    (await get_user_items()).forEach(function (item) {
        if (this_item.uuid === item.uuid) {
            this_item = item;
        }
    });
    let pre = document.getElementById("item");
    pre.innerText = JSON.stringify(this_item, null, 2);
    await dynamic_buttons();
}

async function dynamic_buttons() {
    let sess = await get_sess();
    document.getElementById("buttons").innerText = "";
    if (this_item.status === "transit" && this_item.user_uuids[this_item.user_uuids.length-1] === sess["uuid"]) {
        let btn = document.createElement("input");
        btn.id = "accept_transfer_btn";
        btn.type = "submit";
        btn.value = "Accept This Item Into Inventory";
        btn.addEventListener("click", accept_this_item, false);
        document.getElementById("buttons").appendChild(btn);
        btn = document.createElement("input");
        btn.id = "reject_transfer_btn";
        btn.type = "submit";
        btn.value = "Reject This Item (Sending It back To The Sender)";
        btn.addEventListener("click", reject_this_item, false);
        document.getElementById("buttons").appendChild(btn);
    }
    if (this_item.status === "stationary" && this_item.user_uuids[this_item.user_uuids.length-1] === sess["uuid"]) {
        let btn = document.createElement("input");
        btn.id = "split_btn";
        btn.type = "submit";
        btn.value = "Split This Item";
        btn.addEventListener("click", start_split, false);
        document.getElementById("buttons").appendChild(btn);
        btn = document.createElement("input");
        btn.id = "transfer_btn";
        btn.type = "submit";
        btn.value = "Transfer This Item";
        btn.addEventListener("click", transfer_this_item_start, false);
        document.getElementById("buttons").appendChild(btn);
        btn = document.createElement("input");
        btn.type = "submit";
        btn.value = "Delete This Item";
        btn.addEventListener("click", drop_this_item, false);
        document.getElementById("buttons").appendChild(btn);
        let buttons = document.getElementById("buttons");
        buttons.appendChild(document.createElement("hr"));
        let label1 = document.createElement("label");
        label1.innerText = "Clarity: ";
        buttons.append(label1);
        let selector1 = document.createElement("select");
        selector1.id = "clarity";
        let opt1 = document.createElement("option");
        opt1.value = "flawless (FL)";
        opt1.innerText = "flawless (FL)";
        selector1.add(opt1);
        let opt2 = document.createElement("option");
        opt2.value = "internally flawless (IF)";
        opt2.innerText = "internally flawless (IF)";
        selector1.add(opt2);
        let opt3 = document.createElement("option");
        opt3.value = "very, very slightly included 1 (VVS1)";
        opt3.innerText = "very, very slightly included 1 (VVS1)";
        selector1.add(opt3);
        let opt4 = document.createElement("option");
        opt4.value = "very, very slightly included 2 (VVS2)";
        opt4.innerText = "very, very slightly included 2 (VVS2)";
        selector1.add(opt4);
        let opt5 = document.createElement("option");
        opt5.value = "very slightly included 1 (VS1)";
        opt5.innerText = "very slightly included 1 (VS1)";
        selector1.add(opt5);
        let opt6 = document.createElement("option");
        opt6.value = "very slightly included 2 (VS2)";
        opt6.innerText = "very slightly included 2 (VS2)";
        selector1.add(opt6);
        let opt7 = document.createElement("option");
        opt7.value = "slightly included 1 (SI1)";
        opt7.innerText = "slightly included 1 (SI1)";
        selector1.add(opt7);
        let opt8 = document.createElement("option");
        opt8.value = "slightly included 2 (SI2)";
        opt8.innerText = "slightly included 2 (SI2)";
        selector1.add(opt8);
        let opt9 = document.createElement("option");
        opt9.value = "included 1 (I1)";
        opt9.innerText = "included 1 (I1)";
        selector1.add(opt9);
        let opt10 = document.createElement("option");
        opt10.value = "included 2 (I2)";
        opt10.innerText = "included 2 (I2)";
        selector1.add(opt10);
        let opt11 = document.createElement("option");
        opt11.value = "included 3 (I3)";
        opt11.innerText = "included 3 (I3)";
        selector1.add(opt11);
        buttons.appendChild(selector1);
        let submit1 = document.createElement("input");
        submit1.type = "submit";
        submit1.id = "clarity_submit";
        submit1.innerText = "Commit Change";
        submit1.addEventListener("click", set_clarity, false);
        buttons.appendChild(submit1);
        buttons.appendChild(document.createElement("br"));
        let label2 = document.createElement("label");
        label2.innerText = "Color: ";
        buttons.append(label2);
        let selector2 = document.createElement("select");
        selector2.id = "color";
        let opts = "DEFGHIJKLMNOPQRSTUVWXYZ";
        for (let i = 0; i < opts.length; i++) {
            let opt = document.createElement("option");
            opt.value = opts.charAt(i).toString();
            opt.innerText = opts.charAt(i).toString();
            selector2.add(opt);
        }
        buttons.appendChild(selector2);
        let submit2 = document.createElement("input");
        submit2.type = "submit";
        submit2.id = "color_submit";
        submit2.innerText = "Commit Change";
        submit2.addEventListener("click", set_color, false);
        buttons.appendChild(submit2);
        buttons.appendChild(document.createElement("br"));
        let label3 = document.createElement("label");
        label3.innerText = "Cut: ";
        buttons.append(label3);
        let selector3 = document.createElement("select");
        selector3.id = "cut";
        opts = ["Excellent", "Very Good", "Good", "Fair", "Poor"];
        for (let i = 0; i < opts.length; i++) {
            let opt = document.createElement("option");
            opt.value = opts[i];
            opt.innerText = opts[i];
            selector3.add(opt);
        }
        buttons.appendChild(selector3);
        let submit3 = document.createElement("input");
        submit3.type = "submit";
        submit3.id = "cut_submit";
        submit3.innerText = "Commit Change";
        submit3.addEventListener("click", set_cut, false);
        buttons.appendChild(submit3);
        buttons.appendChild(document.createElement("br"));
        let label4 = document.createElement("label");
        label4.innerText = "Carat: ";
        buttons.append(label4);
        let input1 = document.createElement("input");
        input1.id = "carat";
        input1.type = "number";
        input1.value = "0.0";
        buttons.appendChild(input1);
        let submit4 = document.createElement("input");
        submit4.type = "submit";
        submit4.id = "carat_submit";
        submit4.innerText = "Commit Change";
        submit4.addEventListener("click", set_carat, false);
        buttons.appendChild(submit4);
        buttons.appendChild(document.createElement("br"));
        let label5 = document.createElement("label");
        label5.innerText = "Price: $";
        buttons.append(label5);
        let input2 = document.createElement("input");
        input2.id = "usd_price";
        input2.type = "number";
        input2.value = "0.0";
        buttons.appendChild(input2);
        let submit5 = document.createElement("input");
        submit5.type = "submit";
        submit5.id = "carat_submit";
        submit5.innerText = "Commit Change";
        submit5.addEventListener("click", set_usd_price, false);
        buttons.appendChild(submit5);
        buttons.appendChild(document.createElement("br"));
        let label6 = document.createElement("label");
        label6.innerText = "Date Of Birth: ";
        buttons.append(label6);
        let input3 = document.createElement("input");
        input3.id = "dob";
        input3.type = "date";
        buttons.appendChild(input3);
        let submit6 = document.createElement("input");
        submit6.type = "submit";
        submit6.id = "dob_submit";
        submit6.innerText = "Commit Change";
        submit6.addEventListener("click", set_dob, false);
        buttons.appendChild(submit6);
        buttons.appendChild(document.createElement("br"));
        let label7 = document.createElement("label");
        label7.innerText = "Tender House: ";
        buttons.append(label7);
        let input4 = document.createElement("input");
        input4.id = "tender_house";
        input4.type = "text";
        buttons.appendChild(input4);
        let submit7 = document.createElement("input");
        submit7.type = "submit";
        submit7.id = "tender_house_submit";
        submit7.innerText = "Commit Change";
        submit7.addEventListener("click", set_tender_house, false);
        buttons.appendChild(submit7);
        buttons.appendChild(document.createElement("br"));
        let label8 = document.createElement("label");
        label8.innerText = "Tender Date: ";
        buttons.append(label8);
        let input5 = document.createElement("input");
        input5.id = "tender_date";
        input5.type = "date";
        buttons.appendChild(input5);
        let submit8 = document.createElement("input");
        submit8.type = "submit";
        submit8.id = "tender_date_submit";
        submit8.innerText = "Commit Change";
        submit8.addEventListener("click", set_tender_date, false);
        buttons.appendChild(submit8);
        buttons.appendChild(document.createElement("br"));
        let label9 = document.createElement("label");
        label9.innerText = "Tender House Exchange Rate (ZAR): ";
        buttons.append(label9);
        let input6 = document.createElement("input");
        input6.id = "tender_house_exchange_rate";
        input6.type = "number";
        buttons.appendChild(input6);
        let submit9 = document.createElement("input");
        submit9.type = "submit";
        submit9.id = "tender_house_exchange_rate_submit";
        submit9.innerText = "Commit Change";
        submit9.addEventListener("click", set_tender_house_exchange_rate, false);
        buttons.appendChild(submit9);
        buttons.appendChild(document.createElement("br"));
        let label10 = document.createElement("label");
        label10.innerText = "Cut Date: ";
        buttons.append(label10);
        let input7 = document.createElement("input");
        input7.id = "cut_date";
        input7.type = "date";
        buttons.appendChild(input7);
        let submit10 = document.createElement("input");
        submit10.type = "submit";
        submit10.id = "cut_date_submit";
        submit10.innerText = "Commit Change";
        submit10.addEventListener("click", set_cut_date, false);
        buttons.appendChild(submit10);
        buttons.appendChild(document.createElement("br"));
        let label11 = document.createElement("label");
        label11.innerText = "GIA: ";
        buttons.append(label11);
        let input8 = document.createElement("input");
        input8.id = "gia";
        input8.type = "text";
        buttons.appendChild(input8);
        let submit11 = document.createElement("input");
        submit11.type = "submit";
        submit11.id = "cut_date_submit";
        submit11.innerText = "Commit Change";
        submit11.addEventListener("click", set_gia, false);
        buttons.appendChild(submit11);
        buttons.appendChild(document.createElement("br"));
        let label12 = document.createElement("label");
        label12.innerText = "Finished Jewelery Description: ";
        buttons.append(label12);
        let input9 = document.createElement("input");
        input9.id = "jewelery_description";
        input9.type = "text";
        buttons.appendChild(input9);
        let submit12 = document.createElement("input");
        submit12.type = "submit";
        submit12.id = "jewelery_description_submit";
        submit12.innerText = "Commit Change";
        submit12.addEventListener("click", set_jewelery_description, false);
        buttons.appendChild(submit12);
        buttons.appendChild(document.createElement("br"));

        let label13 = document.createElement("label");
        label13.innerText = "Jewelery #: ";
        buttons.append(label13);
        let input10 = document.createElement("input");
        input10.id = "jewelery_number";
        input10.type = "text";
        buttons.appendChild(input10);
        let submit13 = document.createElement("input");
        submit13.type = "submit";
        submit13.id = "jewelery_number_submit";
        submit13.innerText = "Commit Change";
        submit13.addEventListener("click", set_jewelery_number, false);
        buttons.appendChild(submit13);
        buttons.appendChild(document.createElement("br"));
    }
    if (this_item.status === "transit" && this_item.user_uuids[this_item.user_uuids.length-2] === sess["uuid"]) {
        let btn = document.createElement("input");
        btn.id = "rescind_transfer_btn";
        btn.type = "submit";
        btn.value = "Rescind Transferring This Item";
        btn.addEventListener("click", rescind_this_item, false);
        document.getElementById("buttons").appendChild(btn);
        btn = document.createElement("input");
        btn.id = "redirect_transfer_btn";
        btn.type = "submit";
        btn.value = "Redirect This Item";
        btn.addEventListener("click", start_redirect, false);
        document.getElementById("buttons").appendChild(btn);
    }
}

async function loader() {
    let item = JSON.parse(localStorage.getItem("item_to_show"));
    this_item = item;
    let pre = document.getElementById("item");
    pre.innerText = JSON.stringify(item, null, 2);
    await dynamic_reload();
    await dynamic_buttons();
}

window.onload = loader;