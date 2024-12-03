deleteButtons.forEach((button) => {
    button.addEventListener("click", async (event) => {
        event.preventDefault();

        const mascotaBox = button.closest(".detail_box");
        const id = mascotaBox?.getAttribute("data-id");

        if (!id) {
            console.error("Error: No se encontró el atributo data-id.");
            return;
        }

        console.log(`Enviando solicitud DELETE para ID: ${id}`);

        try {
            const response = await fetch(`/mascotas/${id}`, {
                method: "DELETE",
            });

            console.log("Respuesta del servidor:", response);

            if (!response.ok) {
                const errorData = await response.json();
                console.error("Error en la respuesta del servidor:", errorData);
                alert(`Error: ${errorData.message}`);
                return;
            }

            const result = await response.json();
            console.log("Mascota eliminada exitosamente:", result);
            alert(result.message);

            mascotaBox.remove();
        } catch (error) {
            console.error("Error en el cliente:", error);
            alert("Ocurrió un error al intentar eliminar la mascota.");
        }
    });
});
deleteButtons.forEach((button) => {
    button.addEventListener("click", async (event) => {
        event.preventDefault();

        const mascotaBox = button.closest(".detail_box");
        const id = mascotaBox?.getAttribute("data-id");

        if (!id) {
            console.error("ID no encontrado en el atributo data-id.");
            return;
        }

        if (!confirm("¿Estás seguro de que deseas eliminar esta mascota?")) {
            return;
        }

        try {
            const response = await fetch(`/galeria/eliminar/${id}`, {
                method: "POST",
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
