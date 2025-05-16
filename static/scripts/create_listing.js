const location_select = document.querySelector('#input-location')
const postcode_select = document.querySelector('#input-postcode')
const rooms_select = document.querySelector('#input-rooms')
const bedrooms_select = document.querySelector('#input-bedrooms')
const bathrooms_select = document.querySelector('#input-bathrooms')
const price_input = document.querySelector('#input-price')
const meter_input = document.querySelector('#input-square-meters') // get html elements


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
}); // formatting event listeners

// IMAGE UPLOAD FUNCTIONALITY
const thumbnailUpload = document.querySelector('#choose-thumbnail');
const imageUpload = document.querySelector('#choose-image');
const imageUploadLabel = document.querySelector(`label[for="choose-image"]`);
const thumbnailUploadLabel = document.querySelector(`label[for="choose-thumbnail"]`);
const imagesSeen = new Set(); // to keep track of shown images

const listingImages = [];

const imageContainer = document.querySelector('#image-container');

const updateImageContainer = () => {
    const thumbnail = thumbnailUpload.files[0];
    if (thumbnail) addNewImage(thumbnail);
}

const addNewImage = (file) => {
    if (imagesSeen.has(file.name)) return;
    imagesSeen.add(file.name);
    addImage(file)
}

const addImage = (file) => {
    const reader = new FileReader();
    reader.onload = e => {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.classList.add('asp-3-2')
        img.classList.add('rounded-lg')
        imageContainer.appendChild(img);
    };
    reader.readAsDataURL(file);
}

thumbnailUpload.addEventListener('change', () => {
    updateImageContainer()
    imageUpload.disabled = false;
    imageUploadLabel.classList.remove('disabled-label');
    imageUploadLabel.title = '';
    imageUploadLabel.classList.add('cursor-pointer');
    thumbnailUploadLabel.classList.add('hidden');
})

imageUpload.addEventListener('change', () => {
    for (const file of imageUpload.files) {
        if (!listingImages.some(f => f.name === file.name && f.size === file.size)) {
            listingImages.push(file);
            addNewImage(file);
        }
    }
    updateImageContainer()
    imageUpload.value = ''
}) // image handling

const updateRoomCount = () => {
    const new_value = Number(bedrooms_select.value) + Number(bathrooms_select.value);
    if (new_value >= 0) {
        rooms_select.value = new_value;
    }
}

const form = document.querySelector('form');
form.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    listingImages.forEach(file => formData.append('listing_images', file));

    fetch(form.action, {
        method: 'POST',
        body: formData,
    }).then(response => response.text())
      .then(html => {
          document.open();
          document.write(html);
          document.close();
      });
});

updateRoomCount()