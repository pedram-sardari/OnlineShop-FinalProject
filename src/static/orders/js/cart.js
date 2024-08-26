let cartItemContainerElement = document.getElementById('cart-container')
let addressContainerElement = document.getElementById('address-container')
let changeAddressSelectElement = document.getElementById('change-address-select')
let changeAddressBtn = document.getElementById('change-address-button')
let addAddressBtn = document.getElementById('add-address-button')
let saveSelectedAddressBtn = document.getElementById('save-selected-address')
let closeChangeAddressModalBtn = document.getElementById('closeChangeAddressModal')
let cartAddress = document.getElementById('cart-address')
let createNewAddressFormElement = document.getElementById('create-new-address-form')
let submitFormBtn = document.getElementById('submit-form-button')
let sendFormBtn = document.getElementById('send-form-button')
let submitOrderBtn = document.getElementById('submitOrderButton')
let confirmSubmitOrderModalBtn = document.getElementById('confirm-submit-order-modal-button')
let yesBtn = document.getElementById('yes-button')
let closeSubmitOrderModalBtn = document.getElementById('closeSubmitOrderModal')
let cart;

// urls
let baseURL = `http://${window.location.host}/en/`
let cartURL = baseURL + 'orders/api/v1/cart/'
let authenticationStatusURL = baseURL + 'accounts/api/v1/is-authenticated/'
let submitOrderURL = baseURL + 'orders/api/v1/submit-order/'
let loginURL = baseURL + `accounts/login-email/?next=${baseURL + 'orders/cart/'}`
let userAddressURL = baseURL + 'accounts/api/v1/user-address/'
let cartItemURL = baseURL + 'orders/api/v1/cart-item/'
const payloadCartItem = {
    'store_product': null,
    'quantity': 1,
}

window.addEventListener('load', fetchCart)
saveSelectedAddressBtn.addEventListener('click', saveSelectedAddress)
createNewAddressFormElement.addEventListener('submit', sendCreateNewAddressFormData)
sendFormBtn.addEventListener('click', () => {
    submitFormBtn.click()
})
submitOrderBtn.addEventListener('click', submitOrder)
yesBtn.addEventListener('click', sendSubmitOrder)


function submitOrder() {

    fetch(authenticationStatusURL)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then(data => {
            console.log(data)
            if (data.is_authenticated) {
                confirmSubmitOrderModalBtn.click()
            } else {
                window.location.replace(loginURL);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

}

function sendSubmitOrder() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(submitOrderURL, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
    })
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then(data => {
            console.log(data)
            closeSubmitOrderModalBtn.click()
            fetchCart()
        })
        .catch(error => {
            console.error('Error:', error);
        })
}

function sendCreateNewAddressFormData(event) {
    event.preventDefault();
    let formData = new FormData(this);
    let payload = generateFormDataPayload(formData)
    console.log(payload);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(userAddressURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(payload),
    })
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then(data => {
            console.log(data)
            fetchCustomerAddresses()
            changeAddressBtn.click()
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function generateFormDataPayload(formData) {
    let payload = {}
    for (let pair of formData.entries()) {
        if (pair[0] !== "csrfmiddlewaretoken") {
            // console.log(pair);
            payload[pair[0]] = pair[1]
        }
    }
    return payload
}

function saveSelectedAddress(event) {
    if (changeAddressSelectElement.value) {
        console.log(changeAddressSelectElement.value)
        // update the cart address in backend and reassign the updated cart to the `cart` var
        updateBackendCartAddress(changeAddressSelectElement.value)
    } else {
        console.log('else')
    }
}

function updateBackendCartAddress(selectedCartAddressId) {
    let payload = {
        "user_address": selectedCartAddressId
    }
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(cartURL, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(payload),
    })
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then(data => {
            cart = data
            processCart()
            closeChangeAddressModalBtn.click()
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function fetchCart() {
    fetch(cartURL)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then(backendCart => {
            cart = backendCart
            processCart()
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function processCart() {
    console.log(cart);
    // process user cart address
    if (cart.user_address) {
        displayCartAddress(cart.user_address)
        fetchCustomerAddresses()
    } else {
        addressContainerElement.remove()
    }

    // process user cart items
    fillCartItemContainer(cart.cart_items)
}

function displayCartAddress(address) {
    console.log(address);
    if (address && stringifyAddress(address).trim() !== '') {
        delete address.id
        cartAddress.innerHTML = stringifyAddress(address)
    } else {
        cartAddress.innerHTML = `<p class="text-danger mb-0">هیچ آدرسی برای این سبد خرید ثبت نشده است. </p>`
    }
}

function fetchCustomerAddresses() {
    fetch(userAddressURL)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then(customerAddresses => fillChangeAddressContainer(customerAddresses))
        .catch(error => {
            console.error('Error:', error);
        });
}

function fillChangeAddressContainer(customerAddresses) {
    if (customerAddresses.length > 0) {
        changeAddressSelectElement.innerHTML = ''
        for (let i in customerAddresses) {
            let addressOptionElem = createAddressOptionElem(customerAddresses[i])
            changeAddressSelectElement.innerHTML += addressOptionElem
        }
    } else {
        changeAddressBtn.replaceWith(addAddressBtn)
    }
}


function createAddressOptionElem(address) {
    return ` <option value="${address.id}" >${stringifyAddress(address)}</option> `
}


function fillCartItemContainer(cartItems) {
    cartItemContainerElement.innerHTML = ''
    if (cartItems.length) {
        for (let i in cartItems) {
            console.log(cartItems[i]);
            let cartItemCard = createCartItemElem(cartItems[i])
            cartItemContainerElement.innerHTML = cartItemCard + cartItemContainerElement.innerHTML
        }
    } else {
        vendorsContainerElement.innerHTML = `<p class="text-center text-danger">موجودی این رنگ به پایان رسیده است.</pd>`
    }
}

function createCartItemElem(cartItem) {
    return `
                <div class="cart-item card border shadow-none">
                    <div class="card-body">

                        <div class="d-flex align-items-start border-bottom pb-3">
                            <div class="ms-4">
                                <img src="${cartItem.store_product.image}" alt="" class="avatar-lg rounded">
                            </div>
                            <div class="flex-grow-1 align-self-center overflow-hidden">
                                <div>
                                    <h5 class="text-truncate font-size-18">
                                        <a href="#" class="text-dark">
                                            ${cartItem.store_product.name}
                                        </a>
                                    </h5>
                                    
                                    <p class="text-muted mb-0">
                                        <i class="bx bxs-star text-warning"></i>
                                        <i class="bx bxs-star text-warning"></i>
                                        <i class="bx bxs-star text-warning"></i>
                                        <i class="bx bxs-star text-warning"></i>
                                        <i class="bx bxs-star-half text-warning"></i>
                                    </p>
                                    <p class="mb-0 mt-1">رنگ : <span class="color fw-medium">${cartItem.store_product.color}</span></p>
                                </div>
                            </div>
                            <div class="flex-shrink-0 ms-2">
                                <ul class="list-inline mb-0 font-size-16">
                                    <!-- trash icon -->
                                    <li class="list-inline-item">
                                        <button class="btn btn-outline-danger px-1 " data-store-product-id="${cartItem.store_product.id}" onclick="removeCartItem(event)">
                                            حذف از سبد
                                        </button>
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
<!--                                            <span class="text-muted ms-2">-->
<!--                                                <del class="font-size-16 fw-normal">${2000}</del>-->
<!--                                            </span>-->
                                            <span class="price">
                                                ${numberWithCommas(cartItem.store_product.price)}
                                            </span>
                                            تومان
                                        </h6>
                                    </div>
                                </div>
                                <div class="col-md-5">
                                    <div class="mt-3">
                                        <p class=" text-muted mb-2">تعداد</p>
                                        <div class="d-inline-flex">
                                            <input type="number" class="quantity form-control form-control-sm" data-store-product-id="${cartItem.store_product.id}" value="${cartItem.quantity}" onchange="quantityChanged(event)">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="mt-3">
                                        <p class="text-muted mb-2">جمع</p>
                                        <h6 class="cart-item-sum">${numberWithCommas(cartItem.quantity * cartItem.store_product.price)} تومان</h6>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
                <!-- end card -->
`
}


function removeCartItem(event) {
    event.preventDefault()
    let deleteBtn = event.target
    deleteBtn
        .parentElement
        .parentElement
        .parentElement
        .parentElement
        .parentElement
        .parentElement.remove()

    let storeProductID = deleteBtn.getAttribute('data-store-product-id')
    console.log(storeProductID)
    let cartItem = getCartItemByStoreProductID(storeProductID)
    // console.log(cartItem);
    let newPayloadCartItem = convertToPayloadCartItem(cartItem)
    // console.log(newPayloadCartItem);

    deleteBackendCartItem(newPayloadCartItem)
    // updateCartTotal()
}

function deleteBackendCartItem(cartItem) {
    console.log(cartItem);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(cartItemURL, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(cartItem),
    })
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then(data => console.log(data))
        .catch(error => {
            console.error('Error:', error);
        });

}

function quantityChanged(event) {
    let inputElem = event.target
    if (isNaN(inputElem.value) || inputElem.value <= 0) {
        inputElem.value = 1
    }

    // console.log(inputElem.getAttribute('data-store-product-id'))
    let storeProductID = inputElem.getAttribute('data-store-product-id')
    let cartItem = getCartItemByStoreProductID(storeProductID)
    // console.log(cartItem);
    let newPayloadCartItem = convertToPayloadCartItem(cartItem)
    // console.log(newPayloadCartItem);
    let updatedPayloadCartItem = updateCartItemQuantity(newPayloadCartItem, Number(inputElem.value));
    console.log(updatedPayloadCartItem);

    updateBackendCartItem(updatedPayloadCartItem)
    // updateCartTotal()
}

function getCartItemByStoreProductID(storeProductID) {
    console.log(storeProductID);
    for (let i in cart.cart_items) {
        console.log(cart.cart_items[i].quantity);
        if (cart.cart_items[i].store_product.id === Number(storeProductID)) {
            return cart.cart_items[i]
        }
    }
}

function updateCartItemQuantity(cartItem, newQuantity) {
    cartItem.quantity = newQuantity
    return cartItem
}

function convertToPayloadCartItem(cartItem) {
    let payloadCartItemCopy = {...payloadCartItem}
    payloadCartItemCopy.store_product = JSON.stringify(cartItem.store_product.id)
    return payloadCartItemCopy
}

function updateBackendCartItem(cartItem) {
    console.log(cartItem)
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(cartItemURL, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(cartItem),
    })
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then(data => console.log(data))
        .catch(error => {
            console.error('Error:', error);
        });

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

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function stringifyAddress(address) {
    return Object.values(address)
        .filter(value => value !== null && value !== '')
        .join('-')
}

