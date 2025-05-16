const location_select = document.querySelector('#select-location')
const postcode_select = document.querySelector('#select-postcode')

location_select.addEventListener('change', () => {
    Array.from(postcode_select.options).forEach(postcode => {
        if (postcode.dataset.location !== location_select.value) {
            postcode.classList.add('hidden')
        } else { postcode.classList.remove('hidden')}
    })
    postcode_select.disabled = false;
})

// IMAGE UPLOAD FUNCTIONALITY
const profileUpload = document.querySelector('#choose-profile');
const coverUpload = document.querySelector('#choose-cover');

const imageContainer = document.querySelector('#image-container');

const updateImageContainer = async () => {
    imageContainer.innerHTML = ''
    if (profileUpload.files[0]) {
        const profileDiv = document.createElement('div')
        const profileText = document.createElement('p')
        profileText.textContent = 'prófílmynd'
        const profileImg = await getImage(profileUpload.files[0]);
        imageContainer.appendChild(profileDiv)
        profileDiv.appendChild(profileText)
        profileDiv.appendChild(profileImg)
    }
    if (coverUpload.files[0]) {
        const coverDiv = document.createElement('div')
        const coverText = document.createElement('p')
        coverText.textContent = 'forsíðumynd'
        const coverImg = await getImage(coverUpload.files[0]);
        imageContainer.appendChild(coverDiv)
        coverDiv.appendChild(coverText)
        coverDiv.appendChild(coverImg)
    }
}

profileUpload.addEventListener('change', () => {
    updateImageContainer()
});

coverUpload.addEventListener('change', () => {
    updateImageContainer()
});

const getImage = (file) => {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = e => {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.classList.add('asp-3-2')
            img.classList.add('rounded-lg')
            resolve(img);
        };
        reader.readAsDataURL(file);
    });
}