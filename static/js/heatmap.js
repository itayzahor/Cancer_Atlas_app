document.addEventListener('DOMContentLoaded', function() {
    // Form submission handling
    const form = document.querySelector('form');
    const loadingSpinner = document.getElementById('loading-spinner');

    if (form) {
        form.addEventListener('submit', function(e) {
            loadingSpinner.style.display = 'block';
        });
    }

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Handle filter changes
    const filters = document.querySelectorAll('select, input[type="range"]');
    filters.forEach(filter => {
        filter.addEventListener('change', function() {
            updateFilterDisplay(this);
        });
    });

    function updateFilterDisplay(element) {
        const displayElement = document.getElementById(`${element.id}-value`);
        if (displayElement) {
            displayElement.textContent = element.value;
        }
    }

    // Initialize range slider values
    document.querySelectorAll('input[type="range"]').forEach(updateFilterDisplay);
}); 