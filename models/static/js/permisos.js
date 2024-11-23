$(document).ready(function () {
    loadPermisos(); // Cargar la lista de permisos al inicio

    // Función para cargar permisos
    function loadPermisos() {
        $.get('/permisos/api/permisos')
            .done(function (data) {
                $('#permisos-tbody').empty(); // Limpiar el tbody antes de cargar nuevos datos
                data.forEach(function (permiso) {
                    $('#permisos-tbody').append(`
                        <tr>
                            <td class="text-center">${permiso.permiso_id}</td>
                            <td class="text-center">${permiso.permiso_descripcion}</td>
                            <td class="text-center">
                                <button class='btn btn-warning btn-sm' data-bs-toggle='modal' data-bs-target='#editModal'
                                        data-id='${permiso.permiso_id}' 
                                        data-descripcion='${permiso.permiso_descripcion}' 
                                        data-status='${permiso.permiso_status}'>
                                    <ion-icon name="create"></ion-icon> Modificar
                                </button>
                                <button class='btn btn-danger btn-sm' data-bs-toggle='modal' data-bs-target='#eliminarModal'
                                        data-id='${permiso.permiso_id}' data-descripcion='${permiso.permiso_descripcion}'>
                                    <ion-icon name="trash"></ion-icon> Eliminar
                                </button>
                            </td>
                        </tr>`);
                });
                $('#permisoTable').removeClass('d-none'); // Mostrar la tabla si hay permisos
            })
            .fail(function (xhr) {
                console.error('Error al cargar los permisos:', xhr.responseText);
                alert('Error al cargar los permisos. Ver consola para más detalles.');
            });
    }

    $('#btnAddPermiso').on('click', function () {
        resetForm(); // Reiniciar el formulario al agregar un nuevo permiso
        $('#formPermisos').removeClass('collapse'); // Mostrar el formulario
    });

    // Manejo del envío del formulario de creación y modificación
    $('#formPermisos form').on('submit', function (e) {
        e.preventDefault(); // Evitar el envío tradicional del formulario

        const permiso_id = $('#editId').val(); // Obtener el ID del permiso a editar
        const permisoData = {
            descripcion: $('#descripcion').val(),
            status: $('#status').val(),
        };

        const ajaxSettings = {
            contentType: 'application/json',
            data: JSON.stringify(permisoData),
            error: function (xhr) {
                console.error(permiso_id ? 'Error al actualizar el permiso:' : 'Error al crear el permiso:', xhr.responseText);
                alert(permiso_id ? 'Error al actualizar el permiso. Ver consola para más detalles.' : 'Error al crear el permiso. Ver consola para más detalles.');
            }
        };

        if (permiso_id) { // Si hay un ID, actualiza el permiso
            $.ajax({ ...ajaxSettings, url: `/permisos/api/permisos/${permiso_id}`, type: 'PUT' })
                .done(() => {
                    loadPermisos(); // Recargar la lista de permisos
                    resetForm(); // Reiniciar el formulario
                    $('#editModal').modal('hide'); // Cerrar el modal de edición
                });
        } else { // Si no hay un ID, crea un nuevo permiso
            $.ajax({ ...ajaxSettings, url: '/permisos/api/permisos', type: 'POST' })
                .done(() => {
                    loadPermisos(); // Recargar la lista de permisos
                    resetForm(); // Reiniciar el formulario
                    $('#formPermisos').addClass('collapse'); // Ocultar el formulario
                });
        }
    });

    // Manejo del modal de edición
    $('#editModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#editId').val(button.getAttribute('data-id'));
        $('#editDescripcion').val(button.getAttribute('data-descripcion'));
        $('#editStatus').val(button.getAttribute('data-status'));
    });

    // Manejo del modal de eliminación
    $('#eliminarModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#eliminarId').val(button.getAttribute('data-id'));
        $('#permisoDescripcionEliminar').text(button.getAttribute('data-descripcion'));
    });

    window.deletePermiso = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este permiso?')) {
            $.ajax({
                url: `/permisos/api/permisos/${id}`,
                type: 'DELETE',
                success: function () {
                    loadPermisos(); // Recargar la lista de permisos
                },
                error: function (xhr) {
                    console.error('Error al eliminar el permiso:', xhr.responseText);
                    alert('Error al eliminar el permiso. Ver consola para más detalles.');
                }
            });
        }
    };

    function resetForm() {
        // Reiniciar todos los campos del formulario
        $('#editId').val('');
        $('#descripcion').val('');
        $('#status').val('');
        $('#formPermisos').addClass('collapse'); // Ocultar el formulario
    }

    $('#btnCancel').on('click', resetForm); // Manejar el botón de cancelar
});
