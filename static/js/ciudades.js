$(document).ready(function () {
    loadCiudades(); // Cargar la lista de ciudades al inicio

    // Función para cargar ciudades
    function loadCiudades() {
        $.get('/ciudades/api/ciudades')
            .done(function (data) {
                $('#ciudades-tbody').empty(); // Limpiar el tbody antes de cargar nuevos datos
                data.forEach(function (ciudad) {
                    $('#ciudades-tbody').append(`
                        <tr>
                            <td class="text-center">${ciudad.ciudad_descripcion}</td>
                            <td class="text-center">${ciudad.pais_descripcion}</td>
                            <td class="text-center">
                                <button class='btn btn-warning btn-sm' data-bs-toggle='modal' data-bs-target='#editModal'
                                        data-id='${ciudad.ciudad_id}' 
                                        data-nombre='${ciudad.ciudad_descripcion}' 
                                        data-estado='${ciudad.pais_descripcion}'>
                                    <ion-icon name="create"></ion-icon> Modificar
                                </button>
                                <button class='btn btn-danger btn-sm' data-bs-toggle='modal' data-bs-target='#eliminarModal'
                                        data-id='${ciudad.ciudad_id}' data-nombre='${ciudad.ciudad_descripcion}'>
                                    <ion-icon name="trash"></ion-icon> Eliminar
                                </button>
                            </td>
                        </tr>`);
                });
                $('#ciudadTable').removeClass('d-none'); // Mostrar la tabla si hay ciudades
            })
            .fail(function (xhr) {
                console.error('Error al cargar las ciudades:', xhr.responseText);
                alert('Error al cargar las ciudades. Ver consola para más detalles.');
            });
    }

    $('#btnAddCiudad').on('click', function () {
        resetForm(); // Reiniciar el formulario al agregar una nueva ciudad
        $('#formCiudades').removeClass('collapse'); // Mostrar el formulario
    });

    // Manejo del envío del formulario de creación y modificación
    $('#formCiudades form').on('submit', function (e) {
        e.preventDefault(); // Evitar el envío tradicional del formulario

        const ciudad_id = $('#editId').val(); // Obtener el ID de la ciudad a editar
        const ciudadData = {
            nombre: $('#nombre').val(),
            estado: $('#estado').val(),
        };

        const ajaxSettings = {
            contentType: 'application/json',
            data: JSON.stringify(ciudadData),
            error: function (xhr) {
                console.error(ciudad_id ? 'Error al actualizar la ciudad:' : 'Error al crear la ciudad:', xhr.responseText);
                alert(ciudad_id ? 'Error al actualizar la ciudad. Ver consola para más detalles.' : 'Error al crear la ciudad. Ver consola para más detalles.');
            }
        };

        if (ciudad_id) { // Si hay un ID, actualiza la ciudad
            $.ajax({ ...ajaxSettings, url: `/ciudades/api/ciudades/${ciudad_id}`, type: 'PUT' })
                .done(() => {
                    loadCiudades(); // Recargar la lista de ciudades
                    resetForm(); // Reiniciar el formulario
                    $('#editModal').modal('hide'); // Cerrar el modal de edición
                });
        } else { // Si no hay un ID, crea una nueva ciudad
            $.ajax({ ...ajaxSettings, url: '/ciudades/api/ciudades', type: 'POST' })
                .done(() => {
                    loadCiudades(); // Recargar la lista de ciudades
                    resetForm(); // Reiniciar el formulario
                    $('#formCiudades').addClass('collapse'); // Ocultar el formulario
                });
        }
    });

    // Manejo del modal de edición
    $('#editModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#editId').val(button.getAttribute('data-id'));
        $('#editNombre').val(button.getAttribute('data-nombre'));
        $('#editEstado').val(button.getAttribute('data-estado'));
    });

    // Manejo del modal de eliminación
    $('#eliminarModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#eliminarId').val(button.getAttribute('data-id'));
        $('#ciudadNombreEliminar').text(button.getAttribute('data-nombre'));
    });

    window.deleteCiudad = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar esta ciudad?')) {
            $.ajax({
                url: `/ciudades/api/ciudades/${id}`,
                type: 'DELETE',
                success: function () {
                    loadCiudades(); // Recargar la lista de ciudades
                },
                error: function (xhr) {
                    console.error('Error al eliminar la ciudad:', xhr.responseText);
                    alert('Error al eliminar la ciudad. Ver consola para más detalles.');
                }
            });
        }
    };

    function resetForm() {
        // Reiniciar todos los campos del formulario
        $('#editId').val('');
        $('#nombre').val('');
        $('#estado').val('');
        $('#formCiudades').addClass('collapse'); // Ocultar el formulario
    }

    $('#btnCancel').on('click', resetForm); // Manejar el botón de cancelar
});
