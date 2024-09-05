let searchBtn = document.getElementById('search-btn')
let searchInput = document.getElementById('search-input')
let searchURL = `${window.location.protocol}//${window.location.host}/en/` + 'search/'

searchBtn.addEventListener('click', search)
searchBtn.addEventListener('keypress', search)
console.log(searchBtn)

function search() {
    if (searchInput.value) {
        console.log(searchURL + `?search=${searchInput.value}`)
        window.location.href = searchURL + `?search=${searchInput.value}`;
        // window.location.replace(searchURL + `?search=${searchInput.value}`);
    } else {
        console.log('else')
    }
}