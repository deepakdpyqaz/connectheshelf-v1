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
    return arr;
}

let album = document.querySelector('.album');
let searchbtn = document.querySelector('#searchbtn');
let searchbar = document.querySelector('#searchbar');

function addtocart(e) {
    let distributor = e.target.getAttribute('distributor');
    let bookid = e.target.getAttribute('bookid');
    if (localStorage.hasOwnProperty('distributors')) {
        let distributorlst = arrtostr(localStorage.getItem('distributors'));
        if (distributorlst.includes(distributor)) {
            currentbooks = arrtostr(localStorage.getItem(distributor));
            currentbooks.push(bookid);
            localStorage.setItem(distributor, arrtostr(currentbooks));
        } else {
            distributorlst = arrtostr(localStorage.getItem('distributors'));
            distributorlst.push(distributor);
            localStorage.setItem('distributors', arrtostr(distributorlst));
            currentbooks = [bookid];
            localStorage.setItem(distributor, arrtostr(currentbooks));
        }
    } else {
        distributors = [distributor]
        localStorage.setItem('distributors', arrtostr(distributors));
        currentbooks = [bookid];
        localStorage.setItem(distributor, arrtostr(currentbooks));
    }
    alert("Added to cart");
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

function setalbum(booklist, erase) {
    if (booklist.length == 0) {
        document.querySelector('.main').innerHTML = `<div class="container-fluid">
                <div class="row">
                    <div class="col-md-6 col-sm-12">
                        <div class="row">
                            <div class="col-md-12">
                                <div class="border-rounded-button">
                                    <a href="/reader/request">Make Request</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`;
        return;
    }
    if (erase) {
        document.querySelector('.main').innerHTML = `<section class='bookalbum'></section>'`;
        album = document.querySelector('.bookalbum');
        album.innerHTML = '';
    }
    for (book of booklist) {
        nme = book.name;
        auth = book.author;
        category = book.category;
        price = book.price;
        stock = book.stock;
        bookid = book.bookid;
        photo = book.photo;
        distributor = book.distributor;
        let node = document.createElement('div');
        node.classList.add('bookcard');
        if (stock > 0) {
            if (stock > 1000) {
                stock = 'unlimited';
            }
            let template = `
                <div class="imgfield"><img src="/media/${photo}" alt="${nme}"></div>
                <div class="infofield">
                    <h3>${nme}</h3>
                    <p>Author: ${auth}</p>
                    <p>Price: ${price}</p>
                    <p>Category: ${category}</p>
                    <p>Stock: ${stock}</p>
                </div>
                <div class="actionfield">
                    <button class="addbook" distributor=${distributor} bookid=${bookid}>Add</button>
                </div>`
            node.innerHTML = template;
        } else {
            let template = `
                <div class="imgfield"><img src="/media/${photo}" alt="${nme}"></div>
                <div class="infofield">
                    <h3>${nme}</h3>
                    <p>${auth}</p>
                    <p>${price}</p>
                    <p>${category}</p>
                    <p>${stock}</p>
                </div>
                <div class="actionfield">
                    <button class="addbook btn-secondary" disabled>Out of Stock</button>
                </div>`
            node.innerHTML = template;
        }
        album.appendChild(node);
    }
    let addbook = Array.from(document.querySelectorAll('.addbook'));
    addbook.forEach(elem => {
        elem.addEventListener('click', addtocart);
    })
}

let addbook = Array.from(document.querySelectorAll('.addbook'));
addbook.forEach(elem => {
    elem.addEventListener('click', addtocart);
})



function fetchbooks(params) {
    const Url = '/reader/viewbook'
    parameters = {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
        body: JSON.stringify(params)
    };
    fetch(Url, parameters).then(res => {
        return res.json();
    }).then(res => {
        setalbum(res, true);
        searchbtn.innerText = 'search';
    })
}



//searchbar
document.querySelector('#searchbtn').addEventListener('click', function() {
    let searchquery = document.querySelector('#searchbar').value;
    if (searchquery.length > 0) {
        params = {
            'type': 'search',
            'query': searchquery
        }
        fetchbooks(params);
        searchbtn.innerText = 'searching..';
    }
})

searchbar.addEventListener('keydown', function() {
    setTimeout(function() { searchbtn.click(); }, 5000);
})


//filter
let filterbtn = document.querySelector('#filterbtn');
filterbtn.addEventListener('click', function() {
    let category = document.querySelector('#category').value;
    let author = document.querySelector('#author').value;
    let distributor = document.querySelector('#distributor').value;
    params = {
        'type': 'filter',
        'category': category,
        'author': author,
        'distributor': distributor
    }
    fetchbooks(params);
    $("#filterModal").modal('hide');
})