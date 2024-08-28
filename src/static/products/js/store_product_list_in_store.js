let storeProductData;

// containers
let contentBlockElem = document.getElementById('content-block')
let storeProductContainerElem = document.getElementById('store-product-container')

let storeNameElem =document.getElementById('store-name')

// stores section
let cardGroup = document.getElementById('card-group')
let bestSellerLink = document.getElementById('best-seller-link')
let topRatingLink = document.getElementById('top-rating-link')
let mostExpensiveLink = document.getElementById('recently-created-link')

//pagination
let paginationPreviousBtn = document.getElementById('pagination-previous-btn')
let paginationNextBtn = document.getElementById('pagination-next-btn')
let paginationCurrentPageNumberElem = document.getElementById('pagination-current-page-number')

// urls
let store__slugParam = window.location.search
let baseURL = `http://${window.location.host}/en/`
let storeProductsURL = baseURL + `products/api/v1/store-product/${store__slugParam}`
let bestSellerURL = storeProductsURL + '&ordering=-order_count'
let mostExpensiveURL = storeProductsURL + '&ordering=-price'
let topRatingURL = storeProductsURL + '&ordering=-product__rating_avg'


// event listeners
window.addEventListener('load', fetchStoreProducts)
paginationNextBtn.addEventListener('click', goToNextPage)
paginationPreviousBtn.addEventListener('click', goToPreviousPage)
bestSellerLink.addEventListener('click', (event) => {
    deactivateOrderings()
    bestSellerLink.classList.add('active')
    fetchStoreProducts(event, bestSellerURL)
})

mostExpensiveLink.addEventListener('click', (event) => {
    deactivateOrderings()
    mostExpensiveLink.classList.add('active')
    fetchStoreProducts(event, mostExpensiveURL)
})

topRatingLink.addEventListener('click', (event) => {
    deactivateOrderings()
    topRatingLink.classList.add('active')
    fetchStoreProducts(event, topRatingURL)
})

function fetchStoreProducts(event, url = storeProductsURL) {
    console.log(event);
    console.log(url);
    if (event) {
        event.preventDefault()
    }
    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.json()
            }
        })
        .then(data => {
            storeProductData = data
            createStoreProductsPaginator()
            fillStoresContainer(data.results)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function fillStoresContainer(store_list) {
    console.log(store_list);
    storeNameElem.innerHTML = store_list[0].store
    cardGroup.innerHTML = ''
    for (let i in store_list) {
        cardGroup.innerHTML += createStoreCard(store_list[i])
    }
}

function createStoreCard(storeProduct) {
    return `
            <a href="${storeProduct.url}" style="text-decoration: none">
                <div class="col">
                    <div class="card h-100 position-relative">

                        <!-- Image -->
                        <div class="p-auto" style="height: 200px">
                            <img src="${storeProduct.image}"
                                 class="card-img-top h-100 v-100"
                                 alt="...">
                        </div>
                        <!-- Image -->


                        <div class="card-body" style="height: 130px">
                            <h5 class="card-title text-center">${storeProduct.name}</h5>
                            <!-- rating -->
                            <div class="d-flex justify-content-center my-2">
                                <!-- star icon -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em"
                                     viewBox="0 0 72 72">
                                    <path fill="#FFD700FF"
                                          d="M35.993 10.736L27.791 27.37L9.439 30.044l13.285 12.94l-3.128 18.28l16.412-8.636l16.419 8.624l-3.142-18.278l13.276-12.95l-18.354-2.66z"></path>
                                    <path fill="none" stroke="#000" stroke-linecap="round"
                                          stroke-linejoin="round"
                                          stroke-miterlimit="10" stroke-width="2"
                                          d="M35.993 10.736L27.791 27.37L9.439 30.044l13.285 12.94l-3.128 18.28l16.412-8.636l16.419 8.624l-3.142-18.278l13.276-12.95l-18.354-2.66z"></path>
                                </svg>
                                <!-- star icon -->
                                <p class="card-text fw-bold px-1 mb-0">
                                    ${storeProduct.rating_avg} <span class="fw-light">(${storeProduct.rating_count})</span>
                                </p>
                            </div>
                            <!-- rating -->
                            
                            <!-- discount -->
                            ${createDiscountElem(storeProduct)}
                            <!-- discount -->
                        </div>
                    </div>
                </div>

            </a>
                `
}

function createDiscountElem(storeProduct) {
    if (storeProduct.discounted_price) {
        return `
            <div>
                <p class="card-text text-center text-muted">
                    <del>${numberWithCommas(storeProduct.price)} تومان</del>
                </p>
            </div>
            <div>
                <p class="card-text text-center fw-bold">${numberWithCommas(storeProduct.discounted_price)}
                    تومان</p>
            </div>
`
    } else {
        return `
            <div>
                <p class="card-text text-center">${numberWithCommas(storeProduct.price)} تومان</p>
            </div>
`
    }
}

function createStoreProductsPaginator() {
    if (!storeProductData.links.previous) {
        paginationPreviousBtn.classList.add('disabled')
    } else {
        paginationPreviousBtn.classList.remove('disabled')
    }
    if (!storeProductData.links.next) {
        paginationNextBtn.classList.add('disabled')
    } else {

        paginationNextBtn.classList.remove('disabled')
    }
    if (storeProductData.count) {
        paginationCurrentPageNumberElem.innerHTML = `${storeProductData.current_page} of ${storeProductData.num_pages}`
    }
}

function goToNextPage() {
    if (storeProductData.links.next) {
        fetchStoreProducts(null, storeProductData.links.next)
    }
}

function goToPreviousPage() {
    if (storeProductData.links.previous) {
        fetchStoreProducts(null, storeProductData.links.previous)
    }
}

function deactivateOrderings() {
    bestSellerLink.classList.remove('active')
    topRatingLink.classList.remove('active')
    mostExpensiveLink.classList.remove('active')
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}