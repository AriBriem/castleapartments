document.addEventListener('DOMContentLoaded', function () {


    const toggleBtn = document.querySelectorAll('.filter-button');
    const filterBoxes = document.querySelectorAll('.filter');
    const expandBtnCity = document.querySelectorAll('.expand-button-city');
    const cityCheckboxes = document.querySelectorAll('.city-checkbox');
    const postcodeCheckboxes = document.querySelectorAll('.postcode-checkbox');
    const typeCheckboxes = document.querySelectorAll('.type-checkbox');

    const searchBar = document.querySelector('#search-bar')
    const searchBtn = document.querySelector('#search-button')

    const metersFromSelect = document.querySelector('#meter-from-filter');
    const metersToSelect = document.querySelector('#meter-to-filter');
    const priceFromSelect = document.querySelector('#price-from-filter');
    const priceToSelect = document.querySelector('#price-to-filter');
    const selectFilters = [metersFromSelect, metersToSelect, priceFromSelect, priceToSelect]

    const orderByInputs = document.querySelectorAll('input[name="order-by"]')
    const bookmarkToggle = document.querySelector('#bookmark-toggle')
    const bookMarkIcon = document.querySelector('#bookmark-icon')

    let bookmarkButtons = document.querySelectorAll('.bookmark-button');  // getting html elements

    orderByInputs.forEach(radio => {
        radio.addEventListener('change', () => {
            filterProperties()
        })
    })

    searchBtn.addEventListener('click', () => {
        filterProperties()
    })

    selectFilters.forEach(select => {
        select.addEventListener('change', () => {
            filterProperties();
        })
    })

    typeCheckboxes.forEach(box => {
        box.addEventListener('change', () => {
            filterProperties();
        })
    })

    cityCheckboxes.forEach(cityCheckbox => {
        cityCheckbox.addEventListener('change', () => {
            const id = cityCheckbox.dataset.city;
            const postcodes = document.querySelectorAll(`.postcode-checkbox[data-city="${id}"]`);

            postcodes.forEach(pc => pc.checked = cityCheckbox.checked);
            filterProperties();
        })
    })

    postcodeCheckboxes.forEach(postcodeCheckbox => {
        postcodeCheckbox.addEventListener('change', () => {
            const id = postcodeCheckbox.dataset.city;
            const cityCheckbox = document.querySelector(`.city-checkbox[data-city="${id}"]`)
            const postcodes = document.querySelectorAll(`.postcode-checkbox[data-city="${id}"]`)

            const allChecked = Array.from(postcodes).every(pc => pc.checked);
            const noneChecked = Array.from(postcodes).every(pc => !pc.checked);

            cityCheckbox.checked = allChecked;
            cityCheckbox.indeterminate = !allChecked && !noneChecked;
            filterProperties();
        })
    })

    expandBtnCity.forEach(button => {
        button.addEventListener('click', () => {
            const id = button.dataset.target;
            const list = document.getElementById((id))

            list.classList.toggle('hidden')

            if (button.classList.contains('fa-angle-right')) {
                button.classList.replace('fa-angle-right', 'fa-angle-down')
            } else {
                button.classList.replace('fa-angle-down', 'fa-angle-right')
            }
        })
    })

    toggleBtn.forEach(button => {
        button.addEventListener('click', function (e) {
            e.stopPropagation();
            const filterBox = document.getElementById(button.id.concat('-filter'))
            const hidden = filterBox.parentElement.classList.contains('hidden')
            filterBoxes.forEach(box => {
                box.parentElement.classList.add('hidden')
            })
            if (hidden === true) {
                filterBox.parentElement.classList.remove('hidden');
            }
        });
    })

    bookmarkToggle.addEventListener('click', () => {
        if (bookmarkToggle.dataset.on === 'true') {
            bookMarkIcon.classList.add('far')
            bookMarkIcon.classList.remove('fas')
            bookmarkToggle.dataset.on = 'false'
        } else {
            bookMarkIcon.classList.add('fas')
            bookMarkIcon.classList.remove('far')
            bookmarkToggle.dataset.on = 'true'
        }
        filterProperties()
    }) // adding filter event listeners

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.filter')) {
            filterBoxes.forEach(box => {
                box.parentElement.classList.add('hidden')
            })
        }
    }); // make sure that when you click outside a filter box then it disappears

    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken'); // get csrftoken to send post requests

    const bookmarkListing = (listingId, isBookmarked, btn) => {
        const method = isBookmarked ? 'DELETE' : 'POST';
        const icon = btn.children[0]

        fetch('/bookmark', {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({listingId: listingId})
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error, status: ${response.status}`);
                }
                if (isBookmarked) {
                    icon.classList.add('far')
                    icon.classList.remove('fas')
                    btn.dataset.bookmarked = 'false'
                } else {
                    icon.classList.add('fas')
                    icon.classList.remove('far')
                    btn.dataset.bookmarked = 'true'
                }
            })
    }

    const filterProperties = () => {
        const selectedPostcodes = Array.from(document.querySelectorAll('.postcode-checkbox:checked'))
            .map(pc => pc.value);
        const selectedTypes = Array.from(document.querySelectorAll('.type-checkbox:checked'))
            .map(pc => pc.value);
        const minMeters = metersFromSelect.value;
        const maxMeters = metersToSelect.value;
        const minPrice = priceFromSelect.value;
        const maxPrice = priceToSelect.value;
        const searchValue = searchBar.value;
        const orderBy = document.querySelector('input[name="order-by"]:checked')?.value;
        const filterByBookmark = bookmarkToggle.dataset.on

        const listContainer = document.getElementById('property-list')
        listContainer.classList.add('filter-blur')

        fetch(`/listings/filter/?postcodes=${selectedPostcodes.join(',')}&types=${selectedTypes.join(',')}&meters_from=${minMeters}&meters_to=${maxMeters}&price_from=${minPrice}&price_to=${maxPrice}&search=${searchValue}&order_by=${orderBy}&bookmark=${filterByBookmark}`)
            .then(response => response.text())
            .then(html => {
                listContainer.innerHTML = html;
                listContainer.classList.remove('filter-blur')
                bookmarkButtons = document.querySelectorAll('.bookmark-button')
                bookmarkButtons.forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        e.preventDefault()
                        e.stopPropagation()
                        let isBookmarked = false
                        if (btn.dataset.bookmarked === 'true') {
                            isBookmarked = true
                        }

                        bookmarkListing(btn.dataset.id, isBookmarked, btn)
                    })
                });
            })
    }

    filterProperties();
});