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
    if (imageUrls.length <= i+1) {
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
        const newPos = (index-1+imageUrls.length) % imageUrls.length
        newArr[newPos] = url;
    })
    imageUrls = newArr;
    updateImages()
}

const prevImage = () => {
    const newArr = Array(imageUrls.length)
    imageUrls.forEach((url, index) => {
        const newPos = (index+1+imageUrls.length) % imageUrls.length
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

console.log(imageUrls)

const bookmarkBtn = document.getElementById('bookmark-btn')

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

const bookmarkClicked = (event, listingId) => {
    event.preventDefault()
    event.stopPropagation()
    bookmarkListing(listingId)
}

const bookmarkListing = (listingId) => {
    fetch('/bookmarks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({listingId: listingId})
    })
        .then(res => res.json())
        .then(data => {
            alert('Bookmarked!');
            // Or visually toggle the bookmark icon
        })
        .catch(err => {
            console.error('Failed to bookmark', err);
        });
}