const listContainer = document.querySelector('#seller-listings')
const urlParts = window.location.pathname.split('/');
const sellerId = urlParts[urlParts.length - 2];

const loadListings = () => {
    fetch(`/listings/filter?seller_id=${sellerId}`)
    .then(response => response.text())
    .then(html => {
        listContainer.innerHTML = html;
        listContainer.classList.remove('filter-blur');
    });
}
loadListings();