$(document).ready(function () {
    loadBitacora(); // Cargar la lista de bitácora al inicio

    // Función para cargar bitácora
    function loadBitacora() {
        $.get('/bitacora/api/bitacora')
            .done(function (data) {
                $('#bitacora-tbody').empty(); // Limpiar el tbody antes de cargar nuevos datos
                data.forEach(function (bitacora) {
                    $('#bitacora-tbody').append(`
                        <tr>
                            <td class="text-center">${bitacora.bitacora_id}</td>
                            <td class="text-center">${bitacora.bitacora_descripcion}</td>
                            <td class="text-center">${bitacora.tabla_id}</td>
                            <td class="text-center">${bitacora.bitacora_status}</td>
                            <td class="text-center">${bitacora.bitacora_fechamodificacion}</td>
                            <td class="text-center">
                                <button class='btn btn-warning btn-sm' data-bs-toggle='modal' data-bs-target='#editModal'
                                        data-id='${bitacora.bitacora_id}' 
                                        data-descripcion='${bitacora.bitacora_descripcion}' 
                                        data-tabla='${bitacora.tabla_id}' 
                                        data-status='${bitacora.bitacora_status}'>
                                    <ion-icon name="create"></ion-icon> Modificar
                                </button>
                                <button class='btn btn-danger btn-sm' data-bs-toggle='modal' data-bs-target='#eliminarModal'
                                        data-id='${bitacora.bitacora_id}' data-descripcion='${bitacora.bitacora_descripcion}'>
                                    <ion-icon name="trash"></ion-icon> Eliminar
                                </button>
                            </td>
                        </tr>`);
                });
                $('#bitacoraTable').removeClass('d-none'); // Mostrar la tabla si hay registros
            })
            .fail(function (xhr) {
                console.error('Error al cargar la bitácora:', xhr.responseText);
                alert('Error al cargar la bitácora. Ver consola para más detalles.');
            });
    }

    $('#btnAddBitacora').on('click', function () {
        resetForm(); // Reiniciar el formulario al agregar un nuevo registro
        $('#formBitacora').removeClass('collapse'); // Mostrar el formulario
    });

    // Manejo del envío del formulario de creación y modificación
    $('#formBitacora form').on('submit', function (e) {
        e.preventDefault(); // Evitar el envío tradicional del formulario

        const bitacora_id = $('#editId').val(); // Obtener el ID del registro a editar
        const bitacoraData = {
            descripcion: $('#descripcion').val(),
            tabla: $('#tabla').val(),
            status: $('#status').val(),
        };

        const ajaxSettings = {
            contentType: 'application/json',
            data: JSON.stringify(bitacoraData),
            error: function (xhr) {
                console.error(bitacora_id ? 'Error al actualizar la bitácora:' : 'Error al crear la bitácora:', xhr.responseText);
                alert(bitacora_id ? 'Error al actualizar la bitácora. Ver consola para más detalles.' : 'Error al crear la bitácora. Ver consola para más detalles.');
            }
        };

        if (bitacora_id) { // Si hay un ID, actualiza la bitácora
            $.ajax({ ...ajaxSettings, url: `/bitacora/api/bitacora/${bitacora_id}`, type: 'PUT' })
                .done(() => {
                    loadBitacora(); // Recargar la lista de bitácora
                    resetForm(); // Reiniciar el formulario
                    $('#editModal').modal('hide'); // Cerrar el modal de edición
                });
        } else { // Si no hay un ID, crea un nuevo registro
            $.ajax({ ...ajaxSettings, url: '/bitacora/api/bitacora', type: 'POST' })
                .done(() => {
                    loadBitacora(); // Recargar la lista de bitácora
                    resetForm(); // Reiniciar el formulario
                    $('#formBitacora').addClass('collapse'); // Ocultar el formulario
                });
        }
    });

    // Manejo del modal de edición
    $('#editModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#editId').val(button.getAttribute('data-id'));
        $('#descripcion').val(button.getAttribute('data-descripcion'));
        $('#tabla').val(button.getAttribute('data-tabla'));
        $('#status').val(button.getAttribute('data-status'));
    });

    // Manejo del modal de eliminación
    $('#eliminarModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#eliminarId').val(button.getAttribute('data-id'));
        $('#bitacoraDescripcionEliminar').text(button.getAttribute('data-descripcion'));
    });

    window.deleteBitacora = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este registro de bitácora?')) {
            $.ajax({
                url: `/bitacora/api/bitacora/${id}`,
                type: 'DELETE',
                success: function () {
                    loadBitacora(); // Recargar la lista de bitácora
                },
                error: function (xhr) {
                    console.error('Error al eliminar la bitácora:', xhr.responseText);
                    alert('Error al eliminar la bitácora. Ver consola para más detalles.');
                }
            });
        }
    };

    function resetForm() {
        // Reiniciar todos los campos del formulario
        $('#editId').val('');
        $('#descripcion').val('');
        $('#tabla').val('');
        $('#status').val('');
        $('#formBitacora').addClass('collapse'); // Ocultar el formulario
    }

    $('#btnCancel').on('click', resetForm); // Manejar el botón de cancelar
});
