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