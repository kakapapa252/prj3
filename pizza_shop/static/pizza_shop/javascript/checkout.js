document.addEventListener('DOMContentLoaded', (event) => {
    setinitialContext();

    document.querySelector(".close-floatingbutton").onclick = (e) => {
        document.querySelector(".floatint-area").style.display = 'none';
    }

    document.querySelectorAll(".remove").forEach(item => {
        item.onclick = (e) => {
            var ele = e.srcElement;
            var param = 'param={"removeorderId":"' + ele.parentElement.querySelector(".itemid").innerHTML + '"}';
            var csrftoken = getCookie('csrftoken');
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = (data) => {
                if (xhttp.readyState === XMLHttpRequest.DONE) {
                    window.location.href = "http://127.0.0.1:8000/checkout";
                }
            };
            xhttp.open("POST", "http://127.0.0.1:8000/removeitem/", true);
            xhttp.setRequestHeader("X-CSRFToken", csrftoken);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send(param)
        }
    })

    document.querySelector(".checkout-bt").onclick = (e) => {
        let userlogin = document.querySelector(".display-name").innerHTML;
        if (userlogin.trim() == "") {
            alert("Please login/signup to complete order.")
        } else {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = (data) => {
                if (xhttp.readyState === XMLHttpRequest.DONE) {
                    returnObject = JSON.parse(data.srcElement.response);
                    if (returnObject["success"] == 1)
                        window.location.href = "http://127.0.0.1:8000/";

                }
            };
            xhttp.open("GET", "http://127.0.0.1:8000/completeorder/", true);
            xhttp.send();
        }
    }

    document.querySelector(".logout").onclick = (e) => {
        var csrftoken = getCookie('csrftoken');
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = (data) => {
            if (xhttp.readyState === XMLHttpRequest.DONE) {
                returnObject = JSON.parse(data.srcElement.response);
                if (returnObject["success"] == "1")
                    window.location.href = "http://127.0.0.1:8000/";
            }
        };
        xhttp.open("POST", "http://127.0.0.1:8000/logout/", true);
        xhttp.setRequestHeader("X-CSRFToken", csrftoken);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send();
    }

    document.querySelector(".login").onclick = (e) => {
        let leftwidth = e.srcElement.offsetLeft + e.srcElement.offsetWidth;
        document.querySelector(".floatint-area").style.display = 'block';
        document.querySelector(".signupform").style.display = 'none';
        document.querySelector(".toppingform").style.display = 'none';
        document.querySelector(".loginform").style.display = 'block';
        document.querySelector(".floatint-area").style.top = e.srcElement.offsetTop + e.srcElement.offsetHeight + "px";
        document.querySelector(".floatint-area").style.left = leftwidth - document.querySelector(".floatint-area").offsetWidth + "px";
    }
    document.querySelector(".signup").onclick = (e) => {
        let leftwidth = e.srcElement.offsetLeft + e.srcElement.offsetWidth;
        document.querySelector(".floatint-area").style.display = 'block';
        document.querySelector(".signupform").style.display = 'block';
        document.querySelector(".toppingform").style.display = 'none';
        document.querySelector(".loginform").style.display = 'none';
        document.querySelector(".floatint-area").style.top = e.srcElement.offsetTop + e.srcElement.offsetHeight + "px";
        document.querySelector(".floatint-area").style.left = leftwidth - document.querySelector(".floatint-area").offsetWidth + "px";
    }
});

function setinitialContext() {
    let userlogin = document.querySelector(".display-name").innerHTML;
    if (userlogin.trim() == "")
        setLoginAndLogoutInfo("block", "none");
    else
        setLoginAndLogoutInfo("none", "block");
    document.querySelector(".cart").style.display = "none"
    document.querySelector(".navbar-brand").style.display = "block";
    document.querySelector(".checkout").style.display = "none";
}

function setLoginAndLogoutInfo(login, logout) {
    document.querySelector(".login").style.display = login;
    document.querySelector(".signup").style.display = login;
    document.querySelector(".welcomr-msg").style.display = logout;
    document.querySelector(".logout").style.display = logout;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}