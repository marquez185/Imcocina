document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll(".fav-form");
    forms.forEach(form => {
        const checkbox = form.querySelector(".favorito-checkbox");
        checkbox.addEventListener("change", function() {
            const recetaId = form.getAttribute("data-receta-id");
            const recetaTitulo = form.getAttribute("data-receta-titulo");
            const recetaImagen = form.getAttribute("data-receta-imagen");
            const isChecked = checkbox.checked;

            fetch("{% url 'recetas:ToggleFavorito' %}", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": "{{ csrf_token }}"
                },
                body: JSON.stringify({
                    receta_id: recetaId,
                    receta_titulo: recetaTitulo,
                    receta_imagen: recetaImagen,
                    receta_url: recetaId,  // Incluir la URL de la receta
                    is_checked: isChecked
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    });
});