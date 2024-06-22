let timeout;

document.getElementById('toggle-filters-button').addEventListener('click', function() {
    const filterContainer = document.querySelector('.filter-container');
    const caloriesValues = document.getElementById('calories-values');
    const caloriesSlider = document.getElementById('calories-slider');
    
    if (filterContainer.style.display === 'none' || !filterContainer.style.display) {
        filterContainer.style.display = 'block';
        caloriesValues.classList.remove('hidden');
        caloriesSlider.classList.remove('hidden');
    } else {
        filterContainer.style.display = 'none';
        caloriesValues.classList.add('hidden');
        caloriesSlider.classList.add('hidden');
    }
});

// Mantener la lógica de mostrar/ocultar opciones de filtro existente
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

noUiSlider.create(caloriesSliderElement, {
    start: [0, 2000],
    connect: true,
    range: {
        'min': 0,
        'max': 2000
    },
    step: 10
});

caloriesSliderElement.noUiSlider.on('update', function (values, handle) {
    if (handle === 0) {
        caloriesMin.innerHTML = `${Math.round(values[0])} calorías`;
    } else {
        caloriesMax.innerHTML = `${Math.round(values[1])} calorías`;
    }
});

// Inicializa los valores de visualización
caloriesMin.innerHTML = '0 calorías';
caloriesMax.innerHTML = '2000 calorías';
