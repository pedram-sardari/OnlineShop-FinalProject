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

//cart status
let goodsTotalAmountElem = document.getElementById('goods-total-amount')
let profitAmountElem = document.getElementById('profit-amount')
let finalAmountElem = document.getElementById('final-amount')

let cart;

// urls
let baseURL = `${window.location.protocol}//${window.location.host}/en/`
let cartURL = baseURL + 'orders/api/v1/cart/'
let authenticationStatusURL = baseURL + 'accounts/api/v1/is-authenticated/'
let submitOrderURL = baseURL + 'orders/api/v1/submit-order/'
let loginURL = baseURL + `accounts/login-email/?next=${baseURL + 'orders/cart/'}`
let userAddressURL = baseURL + 'accounts/api/v1/user-address/'
let cartItemURL = baseURL + 'orders/api/v1/cart-item/'
const payloadCartItemSample = {
    'store_product': null, //store product id
    'quantity': 0,
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
    // console.log(payload);
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
            payload[pair[0]] = pair[1]
        }
    }
    return payload
}

function saveSelectedAddress(event) {
    if (changeAddressSelectElement.value) {
        // console.log(changeAddressSelectElement.value)
        // update the cart address in backend and reassign the updated cart to the `cart` var
        updateBackendCartAddress(changeAddressSelectElement.value)
    } else {
        // console.log('else')
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
    // console.log(cart);
    // process user cart address
    if (cart.user_address) {
        displayCartAddress(cart.user_address)
        fetchCustomerAddresses()
    } else {
        addressContainerElement.remove()
    }

    // process user cart items
    fillCartItemContainer(cart.cart_items)
    updateCartSatus()
}

function displayCartAddress(address) {
    // console.log(address);
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
            // console.log(cartItems[i]);
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
                                    
                                    <p class="mb-0 mt-1">رنگ : <span class="color fw-medium">${displayColor(cartItem.store_product.color)}</span></p>
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
                                            ${createDiscountElem(cartItem.store_product)}
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
                                        <h6 ><span class="cart-item-total">${numberWithCommas(cartItem.quantity * cartItem.store_product.price)} </span>تومان</h6>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
                <!-- end card -->
`
}


function createDiscountElem(storeProduct) {
    if (storeProduct.discounted_price) {
        return `
            <div>
                <p class="card-text  text-muted">
                    <del>${numberWithCommas(storeProduct.price)} تومان</del>
                </p>
            </div>
            <div>
                <p class="card-text  fw-bold">${numberWithCommas(storeProduct.discounted_price)}
                    تومان</p>
            </div>
`
    } else {
        return `
            <div>
                <p class="card-text ">${numberWithCommas(storeProduct.price)} تومان</p>
            </div>
`
    }
}

function displayColor(color) {
    if (color) {
        return color
    } else {
        return '-'
    }
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
    // console.log(storeProductID)
    let cartItem = getCartItemByStoreProductID(storeProductID)
    // console.log(cartItem);
    let newPayloadCartItem = convertToPayloadCartItem(cartItem)
    // console.log(newPayloadCartItem);

    deleteBackendCartItem(newPayloadCartItem)
    // updateCartTotal()
}

function deleteBackendCartItem(cartItem) {
    // console.log(cartItem);
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
    cartItem.quantity = inputElem.value
    // console.log(cartItem);
    let newPayloadCartItem = convertToPayloadCartItem(cartItem)
    // console.log(newPayloadCartItem);

    updateBackendCartItem(newPayloadCartItem)
    updateCartSatus()
    updateCartItemTotalElem(event)
}

function getCartItemByStoreProductID(storeProductID) {
    // console.log(storeProductID);
    for (let i in cart.cart_items) {
        // console.log(cart.cart_items[i].quantity);
        if (cart.cart_items[i].store_product.id === Number(storeProductID)) {
            return cart.cart_items[i]
        }
    }
}


function convertToPayloadCartItem(cartItem) {
    let payloadCartItemCopy = {...payloadCartItemSample}

    payloadCartItemCopy.store_product = JSON.stringify(cartItem.store_product.id)
    payloadCartItemCopy.quantity = cartItem.quantity
    return payloadCartItemCopy
}

function updateBackendCartItem(cartItem) {
    // console.log(cartItem)
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

function updateCartSatus() {
    calculateFinalAmount()
    calculateGoodsTotalAmount()
    calculateProfitAmount()
}

function calculateFinalAmount() {
    let result = 0
    let price;
    for (const i in cart.cart_items) {
        if (cart.cart_items[i].store_product.discounted_price) {
            price = cart.cart_items[i].store_product.discounted_price
        } else {
            price = cart.cart_items[i].store_product.price
        }
        result += price * cart.cart_items[i].quantity
    }
    finalAmountElem.innerHTML = numberWithCommas(result)
}

function calculateGoodsTotalAmount() {
    let result = 0
    for (const i in cart.cart_items) {
        result += cart.cart_items[i].store_product.price * cart.cart_items[i].quantity
    }
    goodsTotalAmountElem.innerHTML = numberWithCommas(result)

}

function calculateProfitAmount() {
    let finalAmount = finalAmountElem.innerHTML.replace(/,/g, '')
    let goodsTotalAmount = goodsTotalAmountElem.innerHTML.replace(/,/g, '')
    profitAmountElem.innerHTML = numberWithCommas(parseInt(goodsTotalAmount) - parseInt(finalAmount))
}

function updateCartItemTotalElem(event) {
    let quantityInputElem = event.target
    let storeProductID = quantityInputElem.getAttribute('data-store-product-id')
    let cartItem = getCartItemByStoreProductID(storeProductID)

    let cartItemTotalElem = quantityInputElem
        .parentElement
        .parentElement
        .parentElement
        .parentElement
        .getElementsByClassName('cart-item-total')[0]
    let price = cartItem.store_product.discounted_price ? cartItem.store_product.discounted_price : cartItem.store_product.price
    cartItemTotalElem.innerHTML = numberWithCommas(price * cartItem.quantity)

}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function stringifyAddress(address) {
    return Object.values(address)
        .filter(value => value !== null && value !== '')
        .join('-')
}
