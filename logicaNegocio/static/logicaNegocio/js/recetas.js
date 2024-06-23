document.addEventListener("DOMContentLoaded", function() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const forms = document.querySelectorAll(".fav-form");
    forms.forEach(form => {
        const checkbox = form.querySelector(".favorito-checkbox");
        checkbox.addEventListener("change", function() {
            const recetaId = form.getAttribute("data-receta-id");
            const recetaTitulo = form.getAttribute("data-receta-titulo");
            const recetaImagen = form.getAttribute("data-receta-imagen");
            const recetaUrl = recetaId; // Asumimos que recetaId es la URL de la receta
            const isChecked = checkbox.checked;

            fetch("/toggle_favorito/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    receta_id: recetaId,
                    receta_titulo: recetaTitulo,
                    receta_imagen: recetaImagen,
                    receta_url: recetaUrl,
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
