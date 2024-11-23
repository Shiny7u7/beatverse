$(document).ready(function () {
    loadTablas(); // Cargar la lista de tablas al inicio

    // Función para cargar tablas
    function loadTablas() {
        $.get('/tabla/api/tablas')
            .done(function (data) {
                $('#tablas-tbody').empty(); // Limpiar el tbody antes de cargar nuevos datos
                data.forEach(function (tabla) {
                    $('#tablas-tbody').append(`
                        <tr>
                            <td class="text-center">${tabla.tabla_descripcion}</td>
                            <td class="text-center">${tabla.tabla_status}</td>
                            <td class="text-center">
                                <button class='btn btn-warning btn-sm' data-bs-toggle='modal' data-bs-target='#editModal'
                                        data-id='${tabla.tabla_id}' 
                                        data-descripcion='${tabla.tabla_descripcion}' 
                                        data-status='${tabla.tabla_status}'>
                                    <ion-icon name="create"></ion-icon> Modificar
                                </button>
                                <button class='btn btn-danger btn-sm' data-bs-toggle='modal' data-bs-target='#eliminarModal'
                                        data-id='${tabla.tabla_id}' data-descripcion='${tabla.tabla_descripcion}'>
                                    <ion-icon name="trash"></ion-icon> Eliminar
                                </button>
                            </td>
                        </tr>`);
                });
                $('#tablaTable').removeClass('d-none'); // Mostrar la tabla si hay tablas
            })
            .fail(function (xhr) {
                console.error('Error al cargar las tablas:', xhr.responseText);
                alert('Error al cargar las tablas. Ver consola para más detalles.');
            });
    }

    $('#btnAddTabla').on('click', function () {
        resetForm(); // Reiniciar el formulario al agregar una nueva tabla
        $('#formTablas').removeClass('collapse'); // Mostrar el formulario
    });

    // Manejo del envío del formulario de creación y modificación
    $('#formTablas form').on('submit', function (e) {
        e.preventDefault(); // Evitar el envío tradicional del formulario

        const tabla_id = $('#editId').val(); // Obtener el ID de la tabla a editar
        const tablaData = {
            descripcion: $('#descripcion').val(),
            status: $('#status').val(),
        };

        const ajaxSettings = {
            contentType: 'application/json',
            data: JSON.stringify(tablaData),
            error: function (xhr) {
                console.error(tabla_id ? 'Error al actualizar la tabla:' : 'Error al crear la tabla:', xhr.responseText);
                alert(tabla_id ? 'Error al actualizar la tabla. Ver consola para más detalles.' : 'Error al crear la tabla. Ver consola para más detalles.');
            }
        };

        if (tabla_id) { // Si hay un ID, actualiza la tabla
            $.ajax({ ...ajaxSettings, url: `/tabla/api/tablas/${tabla_id}`, type: 'PUT' })
                .done(() => {
                    loadTablas(); // Recargar la lista de tablas
                    resetForm(); // Reiniciar el formulario
                    $('#editModal').modal('hide'); // Cerrar el modal de edición
                });
        } else { // Si no hay un ID, crea una nueva tabla
            $.ajax({ ...ajaxSettings, url: '/tabla/api/tablas', type: 'POST' })
                .done(() => {
                    loadTablas(); // Recargar la lista de tablas
                    resetForm(); // Reiniciar el formulario
                    $('#formTablas').addClass('collapse'); // Ocultar el formulario
                });
        }
    });

    // Manejo del modal de edición
    $('#editModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#editId').val(button.getAttribute('data-id'));
        $('#descripcion').val(button.getAttribute('data-descripcion'));
        $('#status').val(button.getAttribute('data-status'));
    });

    // Manejo del modal de eliminación
    $('#eliminarModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#eliminarId').val(button.getAttribute('data-id'));
        $('#tablaNombreEliminar').text(button.getAttribute('data-descripcion'));
    });

    window.deleteTabla = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar esta tabla?')) {
            $.ajax({
                url: `/tabla/api/tablas/${id}`,
                type: 'DELETE',
                success: function () {
                    loadTablas(); // Recargar la lista de tablas
                },
                error: function (xhr) {
                    console.error('Error al eliminar la tabla:', xhr.responseText);
                    alert('Error al eliminar la tabla. Ver consola para más detalles.');
                }
            });
        }
    };

    function resetForm() {
        // Reiniciar todos los campos del formulario
        $('#editId').val('');
        $('#descripcion').val('');
        $('#status').val('');
        $('#formTablas').addClass('collapse'); // Ocultar el formulario
    }

    $('#btnCancel').on('click', resetForm); // Manejar el botón de cancelar
});
