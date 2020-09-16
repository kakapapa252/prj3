let selectedItem = "";
let selectedToppings = [];
let extraItems = [];
let extraLoaded = false;
document.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(() => {
        setinitialContext();
    }, 10);


    document.querySelector(".bt-toppings").onclick = (e) => {
        addItemToCart();
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

    document.querySelector(".close-floatingbutton").onclick = (e) => {
        closefloatdiv();
    }

    document.querySelector(".checkout").onclick = (e) => {
        window.location.href = "http://127.0.0.1:8000/checkout/";
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
    document.onclick = (e) => {
        /*if(!(e.target.className.indexOf("signup") > - 1 ||  e.target.className.indexOf("login") > -1
            || e.target.parentElement.parentNode.parentNode.parentElement.className.indexOf("signupcontent") > -1)){
            document.querySelector(".floatint-area").style.display = 'none';
        }*/
    }
    document.querySelectorAll(".size-price").forEach(function(ele) {
        ele.onclick = (e) => {
            selectedToppings = [];
            // Sub Item id user clicked
            selectedItem = ele.querySelectorAll("span")[0].innerHTML;
            topping = ele.querySelectorAll("span")[1].innerHTML;
            containsExtra = ele.querySelectorAll("span")[2].innerHTML;
            // Menu id user clicked to get all extras for the menu
            menuId = ele.querySelectorAll("span")[3].innerHTML;
            // toppings allowed
            toppingsAllowed = ele.querySelectorAll("span")[4].innerHTML;
            if (toppingsAllowed.toUpperCase() == "TRUE") {
                if (containsExtra.toUpperCase() == "TRUE") {
                    document.querySelector(".bt-toppings-next").style.display = "block";
                    document.querySelector(".bt-toppings-back").style.display = "none";
                    document.querySelector(".bt-toppings").style.display = "none";
                    document.querySelector(".bt-toppings-next").onclick = (e) => {
                        document.querySelector(".toppings-container").style.display = "none";
                        document.querySelector(".extra-container").style.display = "block";
                        document.querySelector(".bt-toppings").style.display = "block";
                        document.querySelector(".bt-toppings-back").style.display = "block";
                        document.querySelector(".bt-toppings-next").style.display = "none";
                        if (!extraLoaded) {
                            document.querySelector(".extra-container").innerHTML = "";
                            document.querySelectorAll(".extra_" + menuId).forEach(function(item) {
                                document.querySelector(".extra-container").innerHTML += item.innerHTML;
                            });
                            attachExtraSelectEvent();
                            checkAndDeselectAllExtraToppingsIfToppingNotSelected();
                            extraLoaded = true;
                        } else {
                            checkAndDeselectAllExtraToppingsIfToppingNotSelected();
                        }
                    };
                    document.querySelector(".bt-toppings-back").onclick = (e) => {
                        document.querySelector(".toppings-container").style.display = "block";
                        document.querySelector(".extra-container").style.display = "none";
                        document.querySelector(".bt-toppings-next").style.display = "block";
                        document.querySelector(".bt-toppings-back").style.display = "none";
                        document.querySelector(".bt-toppings").style.display = "none";
                    };
                } else {
                    document.querySelector(".bt-toppings-next").style.display = "none";
                    document.querySelector(".bt-toppings-back").style.display = "none";
                    document.querySelector(".bt-toppings").style.display = "block";
                }
                extraLoaded = false;
                document.querySelector(".extra-container").style.display = "none";
                document.querySelector(".toppings-container").style.display = "block";
                document.querySelector(".toppings-container").innerHTML = "";
                document.querySelector(".extra-container").style.display = "";
                document.querySelectorAll(".topping_details .topping-item").forEach(function(item) {
                    document.querySelector(".toppings-container").innerHTML += item.outerHTML;
                });
                attachToppingEvent(topping);
                openFloatingDiv(e);
            } else {
                addItemToCart();
            }
        }
    })
});

function setinitialContext() {
    let userlogin = document.querySelector(".display-name").innerHTML;
    if (userlogin.trim() == "")
        setLoginAndLogoutInfo("block", "none");
    else
        setLoginAndLogoutInfo("none", "block");
    document.querySelector(".cart").style.display = "block"
    document.querySelector(".navbar-brand").style.display = "none";

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = (data) => {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            returnObject = JSON.parse(data.srcElement.response);
            document.querySelector(".priceval").innerHTML = returnObject["price"];
            setCheckoutButton();
        }
    };
    xhttp.open("GET", "http://127.0.0.1:8000/loadcurrentcontext/", true);
    xhttp.send();
}



//========Floating div open close==========
function closefloatdiv() {
    document.querySelector(".floatint-area").style.display = 'none';
    selectedToppings = [];
}

function openFloatingDiv(e) {
    let leftwidth = window.innerWidth;
    //let height = window.innerHeight;
    let height = window.innerHeight;

    document.querySelector(".floatint-area").style.display = 'block';
    document.querySelector(".signupform").style.display = 'none';
    document.querySelector(".toppingform").style.display = 'block';
    document.querySelector(".loginform").style.display = 'none';
    document.querySelector(".floatint-area").style.top = ((height / 2) - (document.querySelector(".floatint-area").offsetHeight / 2)) + window.pageYOffset + "px";
    document.querySelector(".floatint-area").style.left = leftwidth / 2 - (document.querySelector(".floatint-area").offsetWidth / 2) + "px";

}
//=========================================


function setLoginAndLogoutInfo(login, logout) {
    document.querySelector(".login").style.display = login;
    document.querySelector(".signup").style.display = login;
    document.querySelector(".welcomr-msg").style.display = logout;
    document.querySelector(".logout").style.display = logout;
}

function setCheckoutButton() {
    if (parseInt(document.querySelector(".priceval").innerHTML, 10) > 0)
        document.querySelector(".checkout").style.display = "block";
    else
        document.querySelector(".checkout").style.display = "none";
}

function addItemToCart() {
    //document.querySelectorAll(".topping-item")
    //var toppings = [];
    var csrftoken = getCookie('csrftoken');
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = (data) => {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            selectedToppings = [];
            returnObject = JSON.parse(data.srcElement.response);
            document.querySelector(".priceval").innerHTML = returnObject["price"];
            closefloatdiv();
            setTimeout(() => {
                var r = confirm("Order added successfully to cart. Do you want to checkout? Click cancel to continue shopping.")
                if (r == true)
                    document.querySelector(".checkout").click();
                else
                    setCheckoutButton();
            }, 1);

        }
    };
    var params = 'param={"itemselected":' + selectedItem + ',"toppings":"' + selectedToppings.join() + '","extraitems":"' + extraItems.join() + '"}';
    xhttp.open("POST", "http://127.0.0.1:8000/addToCart/", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    //text/plain;charset=UTF-8 will send as bytes
    xhttp.send(params);

}

//========Mislenious===============
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
//=================================


//==========Topping and Extra Events=================

function attachToppingEvent() {
    document.querySelectorAll(".toppingcheck").forEach(function(item) {
        item.disabled = false;
        item.onclick = (e) => {
            let val = item.getAttribute("val");
            if (item.checked) {
                selectedToppings.push(val);
                if (selectedToppings.length == parseInt(topping)) {
                    document.querySelectorAll(".toppingcheck").forEach(function(otherItem) {
                        if (!selectedtoppingContains(otherItem.getAttribute("val")))
                            otherItem.disabled = true;
                    });
                }
            } else {
                removeOneItemFromSelectedList(val, false)
                    //selectedToppings.splice(ctr, 1);
                document.querySelectorAll(".toppingcheck").forEach(function(otherItem) {
                    otherItem.disabled = false;
                });
            }
            //item.disabled = true;
        }
    });
}

function checkAndDeselectAllExtraToppingsIfToppingNotSelected() {
    document.querySelectorAll(".extra-container input[type='radio']").forEach(function(item) {
        itemVal = item.value;
        itemgrpid = item.name;
        parentId = item.parentNode.querySelector(".parenttopid")
        parentTopId = parentId.innerHTML;
        if (!selectedtoppingContains(parentTopId) && parentTopId.trim() != '') {
            removeOneItemFromSelectedList(itemVal, true);
            item.disabled = true;
            item.checked = false;
        } else
            item.disabled = false;
    });
}

function attachExtraSelectEvent() {
    document.querySelectorAll(".extra-container input[type='radio']").forEach(function(item) {
        item.onclick = (e) => {
            itemVal = item.value;
            itemgrpid = item.name;
            itemToRemove = "";
            let element = item;
            do {
                element = element.parentNode;
            } while (element.className != "extra-item")
            let itemInGrp = element.querySelectorAll("input[type='radio'], input[name='" + itemgrpid + "']");
            for (let i = 0; i < itemInGrp.length; i++) {
                if (itemInGrp[i].value != itemVal) {
                    itemToRemove = itemInGrp[i].value;
                    break;
                }
            }
            if (itemToRemove != "")
                removeOneItemFromSelectedList(itemToRemove, true);
            extraItems.push(itemVal);
        }
    });
}

function selectedtoppingContains(val) {
    let ctr = 0
    for (; ctr < selectedToppings.length; ctr++) {
        if (selectedToppings[ctr] == val)
            return true;
    }
    return false;
}

function removeOneItemFromSelectedList(val, isExtra) {
    let ctr = 0
    if (isExtra) {
        let extrafound = false;
        for (; ctr < extraItems.length; ctr++) {
            if (extraItems[ctr] == val) {
                extrafound = true;
                break;
            }
        }
        if (extrafound)
            extraItems.splice(ctr, 1);
    } else {
        for (; ctr < selectedToppings.length; ctr++) {
            if (selectedToppings[ctr] == val)
                break;
        }
        selectedToppings.splice(ctr, 1);
    }

}

//==================================================