function arrtostr(object) {
    if (typeof(object) == typeof("")) {
        retobj = object.split('/cts/');
        if (retobj[retobj.length - 1] == '')
            retobj.pop();
        return retobj;
    } else {
        retobj = ''
        for (ob of object) {
            retobj += ob + '/cts/';
        }
        return retobj;
    }
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

let distributors = arrtostr(localStorage.getItem('distributors'));
let distributorlist = document.querySelector('.distributorlist');
for (distributor of distributors) {
    let elem = document.createElement('div');
    elem.classList.add('section-heading');
    const template = `
            <h1>${distributor}</h1>
            <div class="filled-rectangle-button col-md-6">
                <a href="/reader/checkout/${distributor}">Checkout</a>
            </div>`;
    elem.innerHTML = template;
    distributorlist.appendChild(elem);
}

function getbook(bookid) {
    let bookres = null;
    const Url = '/reader/getbook';
    parameters = {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
        body: JSON.stringify({ 'bookid': bookid })
    };
    fetch(Url, parameters).then(res => {
        return res.json();
    }).then(res => {
        const template = ``
    })
    return bookres;
}