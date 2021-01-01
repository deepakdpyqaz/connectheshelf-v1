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

//setting the password field
const hiddeneye = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-slash-fill" viewBox="0 0 16 16">
  <path d="M10.79 12.912l-1.614-1.615a3.5 3.5 0 0 1-4.474-4.474l-2.06-2.06C.938 6.278 0 8 0 8s3 5.5 8 5.5a7.027 7.027 0 0 0 2.79-.588zM5.21 3.088A7.028 7.028 0 0 1 8 2.5c5 0 8 5.5 8 5.5s-.939 1.721-2.641 3.238l-2.062-2.062a3.5 3.5 0 0 0-4.474-4.474L5.21 3.088z"/>
  <path d="M5.525 7.646a2.5 2.5 0 0 0 2.829 2.829l-2.83-2.829zm4.95.708l-2.829-2.83a2.5 2.5 0 0 1 2.829 2.829zm3.171 6l-12-12 .708-.708 12 12-.708.707z"/>
</svg>`;
const visibleeye = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">
  <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
  <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
</svg>`;
let passwordField = Array.from(document.querySelectorAll("input[type=password]"));
passwordField.forEach(elem => {
    let par = elem.parentNode;
    let showbtn = document.createElement('span');
    showbtn.innerHTML = hiddeneye;
    showbtn.classList.add('hiddenpass');
    showbtn.addEventListener('click', function() {
        if (showbtn.classList.contains('hiddenpass')) {
            showbtn.classList.remove('hiddenpass');
            showbtn.classList.add('visiblepass');
            showbtn.innerHTML = visibleeye;
            elem.setAttribute('type', 'text');
        } else {
            showbtn.classList.remove('visiblepass');
            showbtn.classList.add('hiddenpass');
            showbtn.innerHTML = hiddeneye;
            elem.setAttribute('type', 'password');
        }
    })
    par.appendChild(showbtn);
})

//form submission
let form = document.querySelector('.jsform');
let submitUrl = form.getAttribute('action');
let inputs = Array.from(form.querySelectorAll('input'));
inputs = inputs.concat(Array.from(form.querySelectorAll('textarea')));
inputs = inputs.concat(Array.from(form.querySelectorAll('select')));
let submitbtn = form.querySelector("button[type='submit'");
let submitbtntext = submitbtn.innerText;
form.addEventListener('submit', function(e) {
    e.preventDefault();
    let formdata = {}
    inputs.forEach(elem => {
        if (elem.getAttribute('name') != null)
            formdata[elem.getAttribute('name')] = elem.value;
    })
    params = {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
        body: JSON.stringify(formdata)
    };
    fetch(submitUrl, params).then(res => {
        return res.json();
    }).then(res => {
        if (res.verified) {
            //setting the color green
            inputs.forEach(elem => {
                elem.classList.add('success');

            })
            submitbtn.removeAttribute('disabled');
            submitbtn.innerText = 'success';
            //redirecting to the url
            if (res['url']) {
                console.log(res['url']);
                setTimeout(function() {
                    window.location = res['url']
                }, 200);
            }
            if (res['otp']) {
                form.setAttribute('action', res['callback']);
                submitUrl = res['callback']
                let node = document.createElement('div');
                node.classList.add('col-md-6');
                node.innerHTML = `<fieldset><input name="otp" id='otp' type="text" class="form-control" id="username" placeholder="Otp(valid for 15 mins)..." required=""></fieldset>`
                let par = form.querySelector('.row');
                let lastchild = document.querySelector("#lastchild");
                par.removeChild(lastchild);
                par.appendChild(node);
                par.appendChild(lastchild);
                let otpinput = document.getElementById('otp');
                inputs.push(otpinput);
                submitbtn.innerText = 'verify';
                setTimeout(function() {
                    inputs.forEach(elem => {
                        elem.classList.add('error');
                        document.querySelector('.Error p').innerText = 'session timeout'
                        submitbtn.removeAttribute('disabled');
                        submitbtn.innerText = submitbtntext;
                    })
                }, 15 * 60 * 1000);
            }

        } else {
            inputs.forEach(elem => {
                elem.classList.add('error');
                document.querySelector('.Error p').innerHTML = res['error']
                submitbtn.removeAttribute('disabled');
                submitbtn.innerText = submitbtntext;
            })
        }
    });
    submitbtn.setAttribute('disabled', '');
    submitbtn.innerText = 'Please wait..';
})