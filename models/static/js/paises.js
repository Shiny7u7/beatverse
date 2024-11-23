$(document).ready(function () {
    loadPaises(); // Cargar la lista de países al inicio

    // Función para cargar países
    function loadPaises() {
        $.get('/pais/api/paises')
            .done(function (data) {
                $('#paises-tbody').empty(); // Limpiar el tbody antes de cargar nuevos datos
                data.forEach(function (pais) {
                    $('#paises-tbody').append(`
                        <tr>
                            <td class="text-center">${pais.pais_descripcion}</td>
                            <td class="text-center">
                                <button class='btn btn-warning btn-sm' data-bs-toggle='modal' data-bs-target='#editModal'
                                        data-id='${pais.pais_id}' 
                                        data-descripcion='${pais.pais_descripcion}'>
                                    <ion-icon name="create"></ion-icon> Modificar
                                </button>
                                <button class='btn btn-danger btn-sm' data-bs-toggle='modal' data-bs-target='#eliminarModal'
                                        data-id='${pais.pais_id}' data-descripcion='${pais.pais_descripcion}'>
                                    <ion-icon name="trash"></ion-icon> Eliminar
                                </button>
                            </td>
                        </tr>`);
                });
                $('#paisTable').removeClass('d-none'); // Mostrar la tabla si hay países
            })
            .fail(function (xhr) {
                console.error('Error al cargar los países:', xhr.responseText);
                alert('Error al cargar los países. Ver consola para más detalles.');
            });
    }

    $('#btnAddPais').on('click', function () {
        resetForm(); // Reiniciar el formulario al agregar un nuevo país
        $('#formPaises').removeClass('collapse'); // Mostrar el formulario
    });

    // Manejo del envío del formulario de creación y modificación
    $('#formPaises form').on('submit', function (e) {
        e.preventDefault(); // Evitar el envío tradicional del formulario

        const pais_id = $('#editId').val(); // Obtener el ID del país a editar
        const paisData = {
            descripcion: $('#descripcion').val(),
        };

        const ajaxSettings = {
            contentType: 'application/json',
            data: JSON.stringify(paisData),
            error: function (xhr) {
                console.error(pais_id ? 'Error al actualizar el país:' : 'Error al crear el país:', xhr.responseText);
                alert(pais_id ? 'Error al actualizar el país. Ver consola para más detalles.' : 'Error al crear el país. Ver consola para más detalles.');
            }
        };

        if (pais_id) { // Si hay un ID, actualiza el país
            $.ajax({ ...ajaxSettings, url: `/pais/api/paises/${pais_id}`, type: 'PUT' })
                .done(() => {
                    loadPaises(); // Recargar la lista de países
                    resetForm(); // Reiniciar el formulario
                    $('#editModal').modal('hide'); // Cerrar el modal de edición
                });
        } else { // Si no hay un ID, crea un nuevo país
            $.ajax({ ...ajaxSettings, url: '/pais/api/paises', type: 'POST' })
                .done(() => {
                    loadPaises(); // Recargar la lista de países
                    resetForm(); // Reiniciar el formulario
                    $('#formPaises').addClass('collapse'); // Ocultar el formulario
                });
        }
    });

    // Manejo del modal de edición
    $('#editModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#editId').val(button.getAttribute('data-id'));
        $('#editDescripcion').val(button.getAttribute('data-descripcion'));
    });

    // Manejo del modal de eliminación
    $('#eliminarModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#eliminarId').val(button.getAttribute('data-id'));
        $('#paisDescripcionEliminar').text(button.getAttribute('data-descripcion'));
    });

    window.deletePais = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este país?')) {
            $.ajax({
                url: `/pais/api/paises/${id}`,
                type: 'DELETE',
                success: function () {
                    loadPaises(); // Recargar la lista de países
                },
                error: function (xhr) {
                    console.error('Error al eliminar el país:', xhr.responseText);
                    alert('Error al eliminar el país. Ver consola para más detalles.');
                }
            });
        }
    };

    function resetForm() {
        // Reiniciar todos los campos del formulario
        $('#editId').val('');
        $('#descripcion').val('');
        $('#formPaises').addClass('collapse'); // Ocultar el formulario
    }

    $('#btnCancel').on('click', resetForm); // Manejar el botón de cancelar
});
