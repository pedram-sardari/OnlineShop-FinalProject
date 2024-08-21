let cartItemContainerElement = document.getElementById('cart-container')

let cart = loadLocalStorageCart()
console.log(cart);
console.log(2)

window.addEventListener('load', syncLocalAndBackendCarts)

function syncLocalAndBackendCarts() {
    // fetch > localcart
    // if is_athenticated < merged cart
    // ove
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let url = `http://${window.location.host}/orders/api/v1/sync-local-and-backend-carts/`
    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(cart),
    })
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then(backendCart => console.log(backendCart))
        .catch(error => {
            console.error('Error:', error);
        });
}

function updateCart(backendCart) {
    if (!backendCart) {
        cart = backendCart
    }
}

function fetchCartItems(event) {
    let url = `http://${window.location.host}/products/api/v1/store-product-vendor/?${getQueryString()}`
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json()
        })
        .then(vendors => fillVendorContainer(vendors))
        .catch(error => {
            console.error('Error:', error);
        });
}

function fillCartItemContainer(storeProducts) {
    cartItemContainerElement.innerHTML = ''
    if (storeProducts.length) {
        for (let i in storeProducts) {
            console.log(storeProducts);
            let cartItem = createCartItem(storeProducts[i], cart[i])
            cartItemContainerElement.innerHTML = cartItem + cartItemContainerElement.innerHTML
        }
    } else {
        vendorsContainerElement.innerHTML = `<p class="text-center text-danger">موجودی این رنگ به پایان رسیده است.</pd>`
    }
}

function createCartItem(cartItem, cart) {
    return `
                <div class="cart-item card border shadow-none">
                    <div class="card-body">

                        <div class="d-flex align-items-start border-bottom pb-3">
                            <div class="ms-4">
                                <img src="${20000}" alt="" class="avatar-lg rounded">
                            </div>
                            <div class="flex-grow-1 align-self-center overflow-hidden">
                                <div>
                                    <h5 class="text-truncate font-size-18">
                                        <a href="#" class="text-dark">
                                            ${2000}
                                        </a>
                                    </h5>
                                    
                                    <p class="text-muted mb-0">
                                        <i class="bx bxs-star text-warning"></i>
                                        <i class="bx bxs-star text-warning"></i>
                                        <i class="bx bxs-star text-warning"></i>
                                        <i class="bx bxs-star text-warning"></i>
                                        <i class="bx bxs-star-half text-warning"></i>
                                    </p>
                                    <p class="mb-0 mt-1">رنگ : <span class="color fw-medium">${2000}</span></p>
                                </div>
                            </div>
                            <div class="flex-shrink-0 ms-2">
                                <ul class="list-inline mb-0 font-size-16">
                                    <!-- trash icon -->
                                    <li class="list-inline-item">
                                        <a href="#" class=" px-1 fs-4 text-danger" onclick="removeCartItem(event)">
                                            <i class="mdi mdi-trash-can-outline"></i>
                                        </a>
                                    </li>
                                    <!-- trash icon -->
                                </ul>
                            </div>
                        </div>

                        <div>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="mt-3">
                                        <p class="text-muted mb-2">قیمت</p>
                                        <h6 class="mb-0 mt-2">
                                            <span class="text-muted ms-2">
                                                <del class="font-size-16 fw-normal">${2000}</del>
                                            </span>
                                            <span class="price">
                                                ${2000}
                                            </span>
                                            تومان
                                        </h6>
                                    </div>
                                </div>
                                <div class="col-md-5">
                                    <div class="mt-3">
                                        <p class=" text-muted mb-2">تعداد</p>
                                        <div class="d-inline-flex">
                                            <input type="number" class="quantity form-control form-control-sm" onchange="quantityChanged(event)">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="mt-3">
                                        <p class="text-muted mb-2">جمع</p>
                                        <h6 class="cart-item-sum">${20000} تومان</h6>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
                <!-- end card -->
`
}

function loadLocalStorageCart() {
    return JSON.parse(localStorage.getItem(cartKey))
}

function removeCartItem(event) {
    var buttonClicked = event.target
    buttonClicked.parentElement.parentElement.remove()
    updateCartTotal()
}

function quantityChanged(event) {
    let input = event.target
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1
    }
    updateCartTotal()
}

function updateCartTotal() {
    let cartItemContainer = document.getElementsByClassName('cart-items')[0]
    let cartItems = cartItemContainer.getElementsByClassName('cart-item')
    let total = 0
    for (let i = 0; i < cartItems.length; i++) {
        let cartItem = cartItems[i]
        let priceElement = cartItem.getElementsByClassName('cart-price')[0]
        let quantityElement = cartItem.getElementsByClassName('cart-quantity-input')[0]
        let price = parseFloat(priceElement.innerText.replace('$', ''))
        let quantity = quantityElement.value
        total = total + (price * quantity)
    }
    total = Math.round(total * 100) / 100
    document.getElementsByClassName('cart-total-price')[0].innerText = '$' + total
}

