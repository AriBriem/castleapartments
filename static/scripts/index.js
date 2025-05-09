document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('postcode-button');
    const filterBox = document.getElementById('postcode-filter');

    toggleBtn.addEventListener('click', function (e) {
        e.stopPropagation(); // Prevent event bubbling if you add outside click later
        filterBox.classList.toggle('hidden');
    });

    // Optional: Close dropdown when clicking outside
    document.addEventListener('click', function (e) {
        if (!toggleBtn.contains(e.target) && !filterBox.contains(e.target)) {
            filterBox.classList.add('hidden');
        }
    });
});
