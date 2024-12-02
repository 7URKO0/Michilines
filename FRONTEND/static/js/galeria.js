
document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".delete-button");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", async (event) => {
            event.preventDefault();
            console.log("Botón eliminar clickeado");

            const mascotaBox = button.closest(".detail_box");
            const id = mascotaBox.getAttribute("data-id");
            console.log("ID de la mascota a eliminar:", id);

            if (!confirm("¿Estás seguro de que deseas eliminar esta mascota?")) {
                return;
            }

            try {
                const response = await fetch(`/mascotas/${id}`, {
                    method: "DELETE",
                });

                const result = await response.json();

                if (response.ok) {
                    alert(result.message);
                    mascotaBox.remove();
                } else {
                    console.error("Error del servidor:", result);
                    alert("No se pudo eliminar la mascota. " + (result.message || ""));
                }
            } catch (error) {
                console.error("Error en el cliente:", error);
                alert("Ocurrió un error al intentar eliminar la mascota.");
            }
        });
    });
});
