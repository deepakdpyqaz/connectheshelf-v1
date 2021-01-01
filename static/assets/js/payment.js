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

function removeFromArray(arr, obj) {
    let i = 0;
    for (i = 0; i < arr.length; i++) {
        if (arr[i] == obj) {
            break;
        }
    }
    for (i; i < arr.length; i++) {
        arr[i] = arr[i + 1]
    }
    arr.pop();
    console.log(arr);
    return arr;
}
let distributor = document.querySelector('#dist').innerHTML.trim();
let table = document.querySelector('.ordertable tbody');
let orderlist = [];


function setTemplate(obj) {
    for (ob of obj) {
        let node = document.createElement('tr');
        let id = ob.bookid;
        let nme = ob.name;
        let price = ob.price;
        let template = `<td class='id'>${id}</td><td>${nme}</td><td class='price'>${price}</td><td><input class='quantity' type='number' min='1' value=1></td><td><div class="col-md-12"><div class="border-rounded-button delete"><span data='${id}'>Remove</span></div></div></td>`;
        node.innerHTML = template;
        table.appendChild(node);
    }
    totPrice();
    if (table.childElementCount == 0) {
        localStorage.setItem('distributors', arrtostr(removeFromArray(arrtostr(localStorage.getItem('distributors')), distributor)));
        localStorage.removeItem(distributor);
        window.location = '/reader/view_order';
    }
    let delbtn = Array.from(document.querySelectorAll('.delete'))
    delbtn.forEach(elem => {
        elem.addEventListener('click', function(e) {
            let curr = e.target;
            let par = curr.parentNode.parentNode.parentNode.parentNode;
            localStorage.setItem(distributor, arrtostr(removeFromArray(arrtostr(localStorage.getItem(distributor)), curr.getAttribute('data'))));
            table.removeChild(par);
            if (table.childElementCount == 0) {
                localStorage.setItem('distributors', arrtostr(removeFromArray(arrtostr(localStorage.getItem('distributors')), distributor)));
                localStorage.removeItem(distributor);
                window.location = '/reader/view_order';
            }
            totPrice();
        })
    })
    let qty = Array.from(document.querySelectorAll('.quantity'));
    qty.forEach(elem =>
        elem.addEventListener('change', function() {
            totPrice();
        })
    )

}

function totPrice() {
    let price = Array.from(document.querySelectorAll('.price'));
    let quantity = Array.from(document.querySelectorAll('.quantity'));
    let total = 0;
    let i;
    for (i = 0; i < price.length; i++) {
        total += Number(price[i].innerHTML) * Number(quantity[i].value);
    }
    document.querySelector('#totalprice').innerHTML = total;
}

const Url = '/reader/getbook'
params = {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
    body: JSON.stringify({ 'bookid': arrtostr(localStorage.getItem(distributor)) })
}
fetch(Url, params).then(res => {
    return res.json();
}).then(res => {
    setTemplate(res);
})


//formsubmission
try {
    let ctsform = document.querySelector('.ctsform');
    ctsform.addEventListener('submit', function(e) {
        e.preventDefault();
        coupon = ctsform.querySelector('#coupon').value;
        express = ctsform.querySelector('#express');
        if (express.checked) {
            express = 1;
        } else {
            express = 0;
        }
        old = ctsform.querySelector('#old');
        if (old.checked) {
            old = 1;
        } else {
            old = 0;
        }
        address = ctsform.querySelector('#address').value;
        makeorder();
        orders = ctsform.querySelector('#orders').value;
        params = {
            'coupon': coupon,
            'express': express,
            'old': old,
            'address': address,
            'orders': orders
        }
        const formUrl = ctsform.getAttribute('action');
        parameters = {
            method: 'POST',
            headers: { 'content-type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify(params)
        }
        fetch(formUrl, parameters).then(res => {
            return res.json();
        }).then(res => {
            if (!res['success']) {
                document.querySelector('.Error').innerHTML = `<p class="text-danger" style="text-transform: capitalize;">${res['error']}</p>`
            } else {
                document.querySelector('.Error').innerHTML = `<p class="text-success" style="text-transform: capitalize;">Placed Successfully</p>`
                localStorage.removeItem(distributor);
                localStorage.setItem('distributors', arrtostr(removeFromArray(arrtostr(localStorage.getItem('distributors')), distributor)));
                setTimeout(function() {
                    window.location = res['callbackurl']
                })
            }
        })
    })
} catch {}

function makeorder() {
    let textarea = document.querySelector("#orders");
    let books = Array.from(document.querySelectorAll(".id"));
    let qty = Array.from(document.querySelectorAll(".quantity"));
    let i = 0;
    let msg = "";
    for (i = 0; i < books.length; i++) {
        if (qty[i].value > 0) {
            msg += books[i].innerHTML + '/qty/' + qty[i].value + '/cts/';
        }
    }
    textarea.value = msg;
}

let screenshot = document.getElementById('screenshot');
let screenshotpreview = document.getElementById('screenshotpreview');
screenshot.addEventListener('change', function(e) {
    if (e.target.files.length > 0) {
        let src = URL.createObjectURL(e.target.files[0])
        screenshotpreview.setAttribute('src', src);
    }
})
try {
    let otherform = document.querySelector('.otherform');
    otherform.addEventListener('submit', function() {
        makeorder();
        localStorage.removeItem(distributor);
        localStorage.setItem('distributors', arrtostr(removeFromArray(arrtostr(localStorage.getItem('distributors')), distributor)));
    })
} catch {}