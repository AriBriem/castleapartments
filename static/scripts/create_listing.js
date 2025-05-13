const location_select = document.querySelector('#input-location')
const postcode_select = document.querySelector('#input-postcode')
const rooms_select = document.querySelector('#input-rooms')
const bedrooms_select = document.querySelector('#input-bedrooms')
const bathrooms_select = document.querySelector('#input-bathrooms')
const price_input = document.querySelector('#input-price')
const meter_input = document.querySelector('#input-square-meters')

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

meter_input.addEventListener('input', (e) => {
    let value = e.target.value;
    value = value.replace(/\D/g, '');

    e.target.value = value.concat('m²');
    e.target.setSelectionRange(e.target.value.length - 2, e.target.value.length - 2)
})

price_input.addEventListener('input', (e) => {
    let value = e.target.value;

    // Remove all non-digit characters
    value = value.replace(/\D/g, '');

    // Format with commas
    const formatted = value.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

    // Update input
    e.target.value = formatted;
});

updateRoomCount()