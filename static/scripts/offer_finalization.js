
function showPaymentFields(method) {
    document.querySelectorAll('.payment-fields').forEach(div => {
        div.style.display = 'none';
    });
    document.getElementById(method + '-fields').style.display = 'block';
}

