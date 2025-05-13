const location_select = document.querySelector('#input-location')
const postcode_select = document.querySelector('#input-postcode')
const rooms_select = document.querySelector('#input-rooms')
const bedrooms_select = document.querySelector('#input-bedrooms')
const bathrooms_select = document.querySelector('#input-bathrooms')

location_select.addEventListener('change', () => {
    Array.from(postcode_select.options).forEach(postcode => {
        if (postcode.dataset.location !== location_select.value) {
            postcode.classList.add('hidden')
        } else { postcode.classList.remove('hidden')}
    })
    postcode_select.disabled = false;
})

bedrooms_select.addEventListener('change', () => {
    updateRoomCount()
})

bathrooms_select.addEventListener('change', () => {
    updateRoomCount()
})

const updateRoomCount = () => {
    new_value = Number(bedrooms_select.value) + Number(bathrooms_select.value);
    if (new_value >= 0) {
        rooms_select.value = new_value;
    }
}

updateRoomCount()