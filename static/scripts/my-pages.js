const listContainer = document.querySelector('#seller-listings')
const sellerId = listContainer.dataset.userId;

const loadListings = () => {
    fetch(`/listings/filter?seller_id=${sellerId}`)
    .then(response => response.text())
    .then(html => {
        listContainer.innerHTML = html;
        listContainer.classList.remove('filter-blur')
    });
}
loadListings()