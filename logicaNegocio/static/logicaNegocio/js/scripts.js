document.addEventListener('DOMContentLoaded', function() {
    let timeout;

    const toggleButton = document.getElementById('toggle-filters-button');
    const filterContainer = document.querySelector('.filter-container');
    const caloriesValues = document.getElementById('calories-values');
    const caloriesSlider = document.getElementById('calories-slider');
    const caloriesMinInput = document.getElementById('calories-min-input');
    const caloriesMaxInput = document.getElementById('calories-max-input');

    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            if (filterContainer.style.display === 'none' || !filterContainer.style.display) {
                filterContainer.style.display = 'block';
                if (caloriesValues) caloriesValues.classList.remove('hidden');
                if (caloriesSlider) caloriesSlider.classList.remove('hidden');
            } else {
                filterContainer.style.display = 'none';
                if (caloriesValues) caloriesValues.classList.add('hidden');
                if (caloriesSlider) caloriesSlider.classList.add('hidden');
            }
        });
    }

    document.querySelectorAll('.filter-button').forEach(button => {
        if (button.id !== 'toggle-filters-button') {
            button.addEventListener('click', function() {
                const options = this.nextElementSibling;
                options.style.display = 'block';
                clearTimeout(timeout); // Clear any existing timeout to prevent premature hiding
            });

            const options = button.nextElementSibling;
            options.addEventListener('mouseover', function() {
                clearTimeout(timeout); // Clear timeout when mouse is over options
            });

            options.addEventListener('mouseleave', function() {
                timeout = setTimeout(() => {
                    options.style.display = 'none';
                }, 30000); // Hide options after 30 seconds if mouse leaves
            });

            // Event listener to hide options once a selection is made and mark button as active
            options.querySelectorAll('select, input').forEach(input => {
                input.addEventListener('change', function() {
                    if (input.value) {
                        button.classList.add('active');
                    }
                    options.style.display = 'none';
                    clearTimeout(timeout); // Clear timeout on selection
                });
            });
        }
    });

    // Script para inicializar y actualizar el rango de calorías usando noUiSlider
    const caloriesSliderElement = document.getElementById('calories-slider');
    const caloriesMin = document.getElementById('calories-min');
    const caloriesMax = document.getElementById('calories-max');

    if (caloriesSliderElement) {
        noUiSlider.create(caloriesSliderElement, {
            start: [0, 5000],
            connect: true,
            range: {
                'min': 0,
                'max': 5000
            },
            step: 10
        });

        caloriesSliderElement.noUiSlider.on('update', function (values, handle) {
            if (handle === 0) {
                caloriesMin.innerHTML = `${Math.round(values[0])} calorías`;
                caloriesMinInput.value = Math.round(values[0]);
            } else {
                caloriesMax.innerHTML = `${Math.round(values[1])} calorías`;
                caloriesMaxInput.value = Math.round(values[1]);
            }
        });

        // Inicializa los valores de visualización
        caloriesMin.innerHTML = '0 calorías';
        caloriesMax.innerHTML = '5000 calorías';
        caloriesMinInput.value = 0;
        caloriesMaxInput.value = 5000;
    }

    // Lógica para redirigir según la visibilidad de los filtros
    const searchForm = document.getElementById('search-form');
    const searchButton = document.getElementById('search-button');
    const filtrarRecetasUrl = "http://localhost:8000/filtrarRecetas/";  // URL completa para FiltrarRecetas
    const buscarRecetasUrl = "http://localhost:8000/buscarRecetas/";    // URL completa para BuscarRecetas

    searchButton.addEventListener('click', function(event) {
        event.preventDefault(); // Evita el envío del formulario por defecto

        if (filterContainer.style.display === 'block') {
            // Si los filtros están visibles, enviar a FiltrarRecetas
            searchForm.action = filtrarRecetasUrl;
        } else {
            // Si los filtros no están visibles, enviar a BuscarRecetas
            searchForm.action = buscarRecetasUrl;
        }

        searchForm.submit(); // Enviar el formulario
    });
});
