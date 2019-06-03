function user_login() {
    let username = document.getElementById("username").value;
    console.log(username);
    let password = document.getElementById("password").value;
    let sha256 = new jsSHA('SHA-256', 'TEXT');
    sha256.update(password);
    let password_hash = sha256.getHash("HEX");
    sha256 = new jsSHA('SHA-256', 'TEXT');
    sha256.update((username + password_hash));
    let user_id = sha256.getHash("HEX");
    let request = make_request({"user_id": user_id}, "does_user_exist");
    console.log(request);
    // send request here
    let result = {"jsonrpc": "2.0", "result": true, "id": 1};
    if (result["result"]) {
        let xhr = new XMLHttpRequest();
        xhr.open("POST", "/cache/put", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            username: username,
            password_hash: password_hash,
            user_id: user_id
        }));
        window.location.href = 'http://127.0.0.1:5000/home/';
    } else {
        alert("Invalid password or username. Please try again.");
    }
}