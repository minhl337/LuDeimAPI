let storage_base = "http://127.0.0.1:4300";


async function upload_file(file) {
    let formData = new FormData();
    formData.append("file", file);
    return await fetch(
        storage_base + "/put/",
        {
            method: 'POST',
            body: formData,
        }).then(function (resp) {
            return resp.json();
        })
}

async function download_file(filename) {
    return await fetch(storage_base + "/get/" + filename)
}