window.addEventListener('load', updateCartCountBadge)

const cartKey = 'cart'
let cartCountBadgeElement = document.getElementById('cart-count')
function updateCartCountBadge(event) {
    let cart = JSON.parse(localStorage.getItem(cartKey))
    if (!cart) {
        cartCountBadgeElement.innerHTML = 0
    } else {
        cartCountBadgeElement.innerText = cart.length
    }

}
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}