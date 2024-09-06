let storeData;
const pageSize = 5

// containers
let contentBlockElem = document.getElementById('content-block')
let storesContainerElem = document.getElementById('stores-container')
let categoriesContainerElem = document.getElementById('categories-container')
let productsContainerElem = document.getElementById('products-container')

// stores section
let cardGroupStores = document.getElementById('card-group-stores')
let cardGroupStoreProducts = document.getElementById('card-group-store-products')


// urls
let language = window.location.pathname.split('/')[1]
let baseURL = `${window.location.protocol}//${window.location.host}/${language}/`
let storesURL = baseURL + `products/api/v1/store/?page_size=${pageSize}`
let storeDefaultImage = `${window.location.protocol}//${window.location.host}/static/products/img/product-default-image.png`
let storeProductsURL = baseURL + `products/api/v1/store-product/index-page/?page_size=${pageSize}`

// event listeners
window.addEventListener('load', generateAllSections)

function generateAllSections() {
    fetchStores(null)
    fetchStoreProducts(null)
}

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
            fillStoreProductContainer(data.results)
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function fillStoreProductContainer(store_product_list) {
    console.log(store_product_list);
    cardGroupStoreProducts.innerHTML = ''
    if (store_product_list.length > 0) {
        for (let i in store_product_list) {
            cardGroupStoreProducts.innerHTML += createStoreProductCard(store_product_list[i])
        }
    } else {
        cardGroupStoreProducts.innerHTML = '<p class="text-center text-danger flex-grow-1 my-5 py-5">محصولی برای این جستجو پیدا نشد</p>'
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

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
