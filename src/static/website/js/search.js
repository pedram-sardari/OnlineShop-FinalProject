let storeProductData;
let storeData;


// stores section
let cardGroup = document.getElementById('card-group')
let bestSellerLink = document.getElementById('best-seller-link')
let topRatingLink = document.getElementById('top-rating-link')
let mostExpensiveLink = document.getElementById('recently-created-link')

let cardGroupStores = document.getElementById('card-group-stores')
let bestSellerLinkStores = document.getElementById('best-seller-link-stores')
let recentlyCreatedLinkStores = document.getElementById('recently-created-link-stores')
let topRatingLinkStores = document.getElementById('top-rating-link-stores')


//pagination
let paginationPreviousBtn = document.getElementById('pagination-previous-btn')
let paginationNextBtn = document.getElementById('pagination-next-btn')
let paginationCurrentPageNumberElem = document.getElementById('pagination-current-page-number')

let paginationPreviousBtnStores = document.getElementById('pagination-previous-btn-stores')
let paginationNextBtnStores = document.getElementById('pagination-next-btn-stores')
let paginationCurrentPageNumberStoresElem = document.getElementById('pagination-current-page-number-stores')


// urls
let language = window.location.pathname.split('/')[1]
let baseURL = `${window.location.protocol}//${window.location.host}/${language}/`
let queryParams = window.location.search

let storeProductsURL = baseURL + `products/api/v1/store-product/${queryParams}`
let bestSellerURL = storeProductsURL + '&ordering=-order_count'
let mostExpensiveURL = storeProductsURL + '&ordering=-price'
let topRatingURL = storeProductsURL + '&ordering=-product__rating_avg'

let storesURL = baseURL + `products/api/v1/store/${queryParams}`
let bestSellerStoresURL = storesURL + '&ordering=-orders_count'
let recentlyCreatedStoresURL = storesURL + '&ordering=-created_at'
let topRatingStoresURL = storesURL + '?ordering=-rating_avg'
let storeDefaultImage = `${window.location.protocol}//${window.location.host}/static/products/img/product-default-image.png`

// event listeners
window.addEventListener('load', (event) => {
    fetchStoreProducts(event)
    fetchStores(event)
})
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


paginationNextBtnStores.addEventListener('click', goToNextPageStores)
paginationPreviousBtnStores.addEventListener('click', goToPreviousPageStores)
bestSellerLinkStores.addEventListener('click', (event) => {
    event.preventDefault()
    deactivateOrderings()
    bestSellerLinkStores.classList.add('active')
    fetchStores(null, bestSellerStoresURL)
})

recentlyCreatedLinkStores.addEventListener('click', (event) => {
    event.preventDefault()
    deactivateOrderings()
    recentlyCreatedLinkStores.classList.add('active')
    fetchStores(null, recentlyCreatedStoresURL)
})

topRatingLinkStores.addEventListener('click', (event) => {
    event.preventDefault()
    deactivateOrderings()
    topRatingLinkStores.classList.add('active')
    fetchStores(null, topRatingStoresURL)
})

function fetchStores(event, url = storesURL) {
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
            storeData = data
            createStoresPaginator()
            fillStoresContainer(data.results)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function getStoreImage(store) {
    return storeDefaultImage
}

function fillStoresContainer(store_list) {
    console.log(store_list);
    cardGroupStores.innerHTML = ''
    if (store_list.length > 0) {
        for (let i in store_list) {
            cardGroupStores.innerHTML += createStoreCard(store_list[i])
        }
    } else {
        cardGroupStores.innerHTML = '<p class="text-center text-danger flex-grow-1 my-5 py-5">فروشگاهی برای این جستجو پیدا نشد</p>'
    }
}

function createStoreCard(store) {
    return `
            <a href="${store.url}" style="text-decoration: none">
               <div class="col">
                    <div class="card h-100 position-relative">

                        <!-- Image -->
                        <div class="p-auto" style="height: 200px">
                            <img src="${getStoreImage(store)}"
                                 class="card-img-top h-100 v-100"
                                 alt="...">
                        </div>
                        <!-- Image -->


                        <div class="card-body" style="height: 160px">
                            <h5 class="card-title text-center">${store.name}</h5>
                            <!-- rating -->
                            <div class="d-flex justify-content-center my-2">
                                <!-- star icon -->
                                <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em"
                                     viewBox="0 0 72 72">
                                    <path fill="#FFD700FF"
                                          d="M35.993 10.736L27.791 27.37L9.439 30.044l13.285 12.94l-3.128 18.28l16.412-8.636l16.419 8.624l-3.142-18.278l13.276-12.95l-18.354-2.66z"></path>
                                    <path fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round"
                                          stroke-miterlimit="10" stroke-width="2"
                                          d="M35.993 10.736L27.791 27.37L9.439 30.044l13.285 12.94l-3.128 18.28l16.412-8.636l16.419 8.624l-3.142-18.278l13.276-12.95l-18.354-2.66z"></path>
                                </svg>
                                <!-- star icon -->
                                <p class="card-text fw-bold px-1 mb-0">
                                    <span class="fw-light">${store.rating_avg} (<span class="text-muted">${store.rating_count}</span>)</span>
                                </p>
                            </div>
                            <!-- rating -->

                                <div>
                                    <p class="card-text text-center ">${store.product_count} محصول </p>
                                </div>

                                <div>
                                    <p class="card-text text-center ">${store.order_count} سفارش </p>
                                </div>
                                
                                <div>
                                    <p class="card-text text-center ">${store.active_days} روز فعال </p>
                                </div>


                        </div>
                    </div>
                </div>
            </a>
                `
}


function createStoresPaginator() {
    if (!storeData.links.previous) {
        paginationPreviousBtnStores.classList.add('disabled')
    } else {
        paginationPreviousBtnStores.classList.remove('disabled')
    }
    if (!storeData.links.next) {
        paginationNextBtnStores.classList.add('disabled')
    } else {

        paginationNextBtnStores.classList.remove('disabled')
    }
    if (storeData.count) {
        paginationCurrentPageNumberStoresElem.innerHTML = `${storeData.current_page} of ${storeData.num_pages}`
    }
}

function goToNextPageStores() {
    if (storeData.links.next) {
        fetchStores(null, storeData.links.next)
    }
}

function goToPreviousPageStores() {
    if (storeData.links.previous) {
        fetchStores(null, storeData.links.previous)
    }
}

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
            fillStoreProductContainer(data.results)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function fillStoreProductContainer(store_product_list) {
    console.log(store_product_list);
    cardGroup.innerHTML = ''
    if (store_product_list.length > 0) {
        for (let i in store_product_list) {
            cardGroup.innerHTML += createStoreProductCard(store_product_list[i])
        }
    } else {
        cardGroup.innerHTML = '<p class="text-center text-danger flex-grow-1 my-5 py-5">محصولی برای این جستجو پیدا نشد</p>'
    }
}

function createStoreProductCard(storeProduct) {
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
                            <h5 class="card-title text-center" style="white-space: nowrap; overflow: hidden">${storeProduct.name}</h5>
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
