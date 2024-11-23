$(document).ready(function () {
    loadEstados(); // Cargar la lista de estados al inicio

    // Función para cargar estados
    function loadEstados() {
        $.get('/estados/api/estados')
            .done(function (data) {
                $('#estados-tbody').empty(); // Limpiar el tbody antes de cargar nuevos datos
                data.forEach(function (estado) {
                    $('#estados-tbody').append(`
                        <tr>
                            <td class="text-center">${estado.estado_descripcion}</td>
                            <td class="text-center">${estado.ciudad_descripcion}</td>
                            <td class="text-center">
                                <button class='btn btn-warning btn-sm' data-bs-toggle='modal' data-bs-target='#editEstadoModal'
                                        data-id='${estado.estado_id}' 
                                        data-nombre='${estado.estado_descripcion}'>
                                    <ion-icon name="create"></ion-icon> Modificar
                                </button>
                                <button class='btn btn-danger btn-sm' data-bs-toggle='modal' data-bs-target='#eliminarEstadoModal'
                                        data-id='${estado.estado_id}' data-nombre='${estado.estado_descripcion}'>
                                    <ion-icon name="trash"></ion-icon> Eliminar
                                </button>
                            </td>
                        </tr>`);
                });
                $('#estadoTable').removeClass('d-none'); // Mostrar la tabla si hay estados
            })
            .fail(function (xhr) {
                console.error('Error al cargar los estados:', xhr.responseText);
                alert('Error al cargar los estados. Ver consola para más detalles.');
            });
    }

    $('#btnAddEstado').on('click', function () {
        resetForm(); // Reiniciar el formulario al agregar un nuevo estado
        $('#formEstados').removeClass('collapse'); // Mostrar el formulario
    });

    // Manejo del envío del formulario de creación y modificación
    $('#formEstados form').on('submit', function (e) {
        e.preventDefault(); // Evitar el envío tradicional del formulario

        const estado_id = $('#editEstadoId').val(); // Obtener el ID del estado a editar
        const estadoData = {
            descripcion: $('#estadoDescripcion').val(),
        };

        const ajaxSettings = {
            contentType: 'application/json',
            data: JSON.stringify(estadoData),
            error: function (xhr) {
                console.error(estado_id ? 'Error al actualizar el estado:' : 'Error al crear el estado:', xhr.responseText);
                alert(estado_id ? 'Error al actualizar el estado. Ver consola para más detalles.' : 'Error al crear el estado. Ver consola para más detalles.');
            }
        };

        if (estado_id) { // Si hay un ID, actualiza el estado
            $.ajax({ ...ajaxSettings, url: `/estados/api/estados/${estado_id}`, type: 'PUT' })
                .done(() => {
                    loadEstados(); // Recargar la lista de estados
                    resetForm(); // Reiniciar el formulario
                    $('#editEstadoModal').modal('hide'); // Cerrar el modal de edición
                });
        } else { // Si no hay un ID, crea un nuevo estado
            $.ajax({ ...ajaxSettings, url: '/api/estados', type: 'POST' })
                .done(() => {
                    loadEstados(); // Recargar la lista de estados
                    resetForm(); // Reiniciar el formulario
                    $('#formEstados').addClass('collapse'); // Ocultar el formulario
                });
        }
    });

    // Manejo del modal de edición
    $('#editEstadoModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#editEstadoId').val(button.getAttribute('data-id'));
        $('#estadoDescripcion').val(button.getAttribute('data-nombre'));
    });

    // Manejo del modal de eliminación
    $('#eliminarEstadoModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#eliminarEstadoId').val(button.getAttribute('data-id'));
        $('#estadoNombreEliminar').text(button.getAttribute('data-nombre'));
    });

    // Función para eliminar estado
    window.deleteEstado = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este estado?')) {
            $.ajax({
                url: `/estados/api/estados/${id}`,
                type: 'DELETE',
                success: function () {
                    loadEstados(); // Recargar la lista de estados
                },
                error: function (xhr) {
                    console.error('Error al eliminar el estado:', xhr.responseText);
                    alert('Error al eliminar el estado. Ver consola para más detalles.');
                }
            });
        }
    };

    function resetForm() {
        // Reiniciar todos los campos del formulario
        $('#editEstadoId').val('');
        $('#estadoDescripcion').val('');
        $('#formEstados').addClass('collapse'); // Ocultar el formulario
    }

    $('#btnCancel').on('click', resetForm); // Manejar el botón de cancelar
});
