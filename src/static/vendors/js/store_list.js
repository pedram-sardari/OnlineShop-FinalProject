let storeData;

// containers
let contentBlockElem = document.getElementById('content-block')
let storesContainerElem = document.getElementById('stores-container')

// stores section
let cardGroupStores = document.getElementById('card-group-stores')
let bestSellerLinkStores = document.getElementById('best-seller-link-stores')
let topRatingLinkStores = document.getElementById('top-rating-link-stores')
let recentlyCreatedLinkStores = document.getElementById('recently-created-link-stores')

//pagination
let paginationPreviousBtnStores = document.getElementById('pagination-previous-btn-stores')
let paginationNextBtnStores = document.getElementById('pagination-next-btn-stores')
let paginationCurrentPageNumberStoresElem = document.getElementById('pagination-current-page-number-stores')

// urls
let language = window.location.pathname.split('/')[1]
let baseURL = `${window.location.protocol}//${window.location.host}/${language}/`
let storesURL = baseURL + 'products/api/v1/store/'
let bestSellerStoresURL = storesURL + '?ordering=-orders_count'
let recentlyCreatedStoresURL = storesURL + '?ordering=-created_at'
let topRatingStoresURL = storesURL + '?ordering=-rating_avg'
let storeDefaultImage = `${window.location.protocol}//${window.location.host}/static/products/img/product-default-image.png`


// event listeners
window.addEventListener('load', fetchStores)
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
    for (let i in store_list) {
        cardGroupStores.innerHTML += createStoreCard(store_list[i])
    }
}

function createStoreCard(store) {
    return `
            <a href="${store.url}" style="text-decoration: none">
               <div class="col">
                    <div class="card h-100 position-relative">

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

function deactivateOrderings() {
    bestSellerLinkStores.classList.remove('active')
    topRatingLinkStores.classList.remove('active')
    recentlyCreatedLinkStores.classList.remove('active')
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}