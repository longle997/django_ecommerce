// look for all element with class update-cart
var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    // listen to 'click' action on every element with class update-cart
    updateBtns[i].addEventListener('click', function () {
        // data-product={{ product.id }} from store.html
        var productId = this.dataset.product
        // data-action="add" from store.html
        var action = this.dataset.action
        console.log('productID:', productId, ' Action:', action)

        // receiving user variable from main.html
        if (user == 'AnonymousUser') {
            updateCookieOrder(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    console.log("User is authenticated, sending data ...")

    // url that we wanna send request
    var url = 'update-item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        // body contain data we wanna send
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            // console.log('Data', data)
            location.reload()
        });
}

function updateCookieOrder(productId, action) {
    console.log("User is unauthenticated, get from cookie ...")

    if (action == "add") {
        // if there is not cart[productID] => define it
        if (cart[productId] == undefined) {
            cart[productId] = { "quantity": 1 }
        } else {
            cart[productId]["quantity"] += 1
        }
    } else {
        cart[productId]["quantity"] -= 1
        if (cart[productId]["quantity"] <= 0) {
            console.log("Remove cart item: ", cart[productId])
            delete cart[productId]
        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
}