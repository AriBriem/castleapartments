const price_input = document.querySelector('#input-amount')

price_input.addEventListener('input', (e) => {
    let value = e.target.value;

    // Remove all non-digit characters
    value = value.replace(/\D/g, '');

    // Format with commas
    const formatted = value.replace(/\B(?=(\d{3})+(?!\d))/g, ".");

    // Update input
    e.target.value = formatted;
});