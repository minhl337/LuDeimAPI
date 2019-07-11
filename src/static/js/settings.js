function to_locations() {
    window.location.href = url_base + '/website/locations.html';
}

function to_inventory() {
    window.location.href = url_base + '/website/inventory.html';
}

async function restart() {
    logout().then(_ => window.location.href = url_base + '/website/user_login.html');
}

function to_settings() {
    window.location.href = url_base + '/website/settings.html';
}

async function exec_change_avatar() {
    let new_avatar = document.getElementById("new_avatar").value;
    let resp = await change_avatar(new_avatar);
    document.getElementById("new_avatar").value = "";
}

async function exec_change_password() {
    let new_password = document.getElementById("new_password").value;
    let pword_hash = new_password;
    for (let i = 0; i < 8; i++) pword_hash += pword_hash;
    pword_hash = pword_hash.substr(0,128);
    let resp = await change_password_hash(pword_hash);
    document.getElementById("new_password").value = "";
}

async function exec_change_username() {
    let new_username = document.getElementById("new_username").value;
    let resp = await change_username(new_username);
    document.getElementById("new_username").value = "";
}
