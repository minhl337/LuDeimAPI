async function submit() {
    let uname = document.getElementById("uname").value;
    let pword = document.getElementById("pword").value;
    const msgBuffer = new TextEncoder('utf-8').encode(pword);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const pword_hash = hashArray.map(b => ('00' + b.toString(16)).slice(-2)).join('');
    console.log(pword_hash);
    let resp = await login_user(uname, pword_hash);
    window.location.href = url_base + '/website/locations.html'
}
