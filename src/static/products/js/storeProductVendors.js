let colorElement = document.getElementById('id_color');
let vendorsContainerElement = document.getElementById('vendors-container')
let productName = document.getElementById('product-name')
// const storeProductIdData = {'quantity': 1}
const cartItem = {
    'store_product': null,
    'quantity': 1,
}
let cart = {
    "cart_items": [],
    "user_address": ""
}
console.log(cart);

selectFirstOption()
colorElement.addEventListener('change', fetchVendors)

function selectFirstOption() {
    colorElement.firstElementChild.remove()
    if (colorElement.children.length > 0) {
        colorElement.firstElementChild.setAttribute("selected", "")
    } else {
        colorElement.setAttribute('hidden', "")
        colorElement.previousElementSibling.setAttribute('hidden', "")
    }
    fetchVendors()
}


function fetchVendors(event) {
    let url = `${window.location.protocol}//${window.location.host}/en/products/api/v1/store-product-vendor/?${getQueryString()}`
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


function getQueryString() {
    const queryParams = {
        'product_color_id': colorElement.value,
        'product_name': productName.textContent
    }
    return new URLSearchParams(queryParams).toString();
}


function fillVendorContainer(vendors) {
    vendorsContainerElement.innerHTML = ''
    if (vendors.length) {
        for (let i in vendors) {
            let vendor = createVendor(vendors[i])
            vendorsContainerElement.innerHTML += vendor
        }
    } else {
        vendorsContainerElement.innerHTML = `<p class="text-center text-danger">موجودی این رنگ به پایان رسیده است.</pd>`
    }
}

function createVendor(vendor) {
    return `
        <div class="col d-flex justify-content-around border-bottom py-1">
            <input class="store-product-id" type="text"  hidden value="${vendor.id}"/>
            <p class="mb-0 mx-auto">${vendor.store}</p>
            <p class="mb-0 mx-auto">${displayDiscount(vendor.discount)}</p>
            <p class="mb-0 mx-auto">${numberWithCommas(vendor.price)}تومان</p>
            <button class="add-to-cart-button btn btn-danger " onclick="addToCart(event)">افزودن به سبد</button>
        </div>
    `
}


function displayDiscount(discount) {
    if (discount === null) {
        return '-'
    } else {
        return `${discount}%`
    }
}

function addToCart(event) {
    console.log('addToCart');
    console.log(cart);
    let addToCartBtn = event.target
    let storeProductIdElement = addToCartBtn.parentElement.getElementsByClassName('store-product-id')[0]
    let storeProductId = storeProductIdElement.value
    let newCartItem = {...cartItem}
    newCartItem.store_product = storeProductId

    // let cartItemExists = false
    // for (let i in cart.cart_items) {
    //     if (cart.cart_items[i].store_product === newCartItem.store_product) {
    //         cartItemExists = true
    //         break
    //     }
    // }
    // if (!cartItemExists) {
    //     cart.cart_items.push(newCartItem)
    // }

    sendCartItemToServer(newCartItem)
}

function sendCartItemToServer(newCartItem) {

    console.log('sendCartItemToServer');
    console.log(newCartItem);
    let url = `${window.location.protocol}//${window.location.host}/en/orders/api/v1/cart-item/`
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(newCartItem),
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

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}