const bigImage = document.getElementById('image-1')
const smallImage1 = document.getElementById('image-2')
const smallImage2 = document.getElementById('image-3')

const prevImageButton = document.getElementById('prev-image')
const nextImageButton = document.getElementById('next-image')

const imageUrlObjects = JSON.parse(document.getElementById('listing-images').textContent);
let imageUrls = Array()

imageUrls.push(bigImage.src)
imageUrlObjects.forEach(url => {
    imageUrls.push(url)
})
for (let i = 0; i < 2; i++) {
    if (imageUrls.length <= i + 1) {
        imageUrls.push('/media/img/listingimages/defaultimage.jpg');
    }
}

console.log(imageUrls)

const updateImages = () => {
    bigImage.src = imageUrls[0]
    smallImage1.src = imageUrls[1]
    smallImage2.src = imageUrls[2]
}

const nextImage = () => {
    const newArr = Array(imageUrls.length)
    imageUrls.forEach((url, index) => {
        const newPos = (index - 1 + imageUrls.length) % imageUrls.length
        newArr[newPos] = url;
    })
    imageUrls = newArr;
    updateImages()
}

const prevImage = () => {
    const newArr = Array(imageUrls.length)
    imageUrls.forEach((url, index) => {
        const newPos = (index + 1 + imageUrls.length) % imageUrls.length
        newArr[newPos] = url;
    })
    imageUrls = newArr;
    updateImages()
}

prevImageButton.addEventListener('click', () => {
    prevImage()
})

nextImageButton.addEventListener('click', () => {
    nextImage()
})

updateImages()

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
const bookmarkButton = document.querySelector('.bookmark-button');  // getting html elements

bookmarkButton.addEventListener('click', (e) => {
    let isBookmarked = false
    if (bookmarkButton.dataset.bookmarked === 'true') {
        isBookmarked = true
    }
    bookmarkListing(bookmarkButton.dataset.id, isBookmarked, bookmarkButton)
})

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