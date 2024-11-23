$(document).ready(function () {
    loadClientes(); // Cargar la lista de clientes al inicio

    // Función para cargar clientes
    function loadClientes() {
        $.get('/clientes/api/clientes')
            .done(function (data) {
                $('#clientes-tbody').empty(); // Limpiar el tbody antes de cargar nuevos datos
                data.forEach(function (cliente) {
                    $('#clientes-tbody').append(`
                        <tr>
                            <td class="text-center">${cliente.cliente_nombre}</td>
                            <td class="text-center">${cliente.cliente_primerapellido}</td>
                            <td class="text-center">${cliente.cliente_segundoapellido}</td>
                            <td class="text-center">${cliente.cliente_email}</td>
                            <td class="text-center">
                                <button class='btn btn-warning btn-sm' data-bs-toggle='modal' data-bs-target='#editModal'
                                        data-id='${cliente.cliente_id}' 
                                        data-nombre='${cliente.cliente_nombre}' 
                                        data-apellido1='${cliente.cliente_primerapellido}' 
                                        data-apellido2='${cliente.cliente_segundoapellido}' 
                                        data-correo='${cliente.cliente_email}' 
                                        data-contrasena='${cliente.cliente_contrasena}'>
                                    <ion-icon name="create"></ion-icon> Modificar
                                </button>
                                <button class='btn btn-danger btn-sm' data-bs-toggle='modal' data-bs-target='#eliminarModal'
                                        data-id='${cliente.cliente_id}' data-nombre='${cliente.cliente_nombre}'>
                                    <ion-icon name="trash"></ion-icon> Eliminar
                                </button>
                            </td>
                        </tr>`);
                });
                $('#clienteTable').removeClass('d-none'); // Mostrar la tabla si hay clientes
            })
            .fail(function (xhr) {
                console.error('Error al cargar los clientes:', xhr.responseText);
                alert('Error al cargar los clientes. Ver consola para más detalles.');
            });
    }

    $('#btnAddCliente').on('click', function () {
        resetForm(); // Reiniciar el formulario al agregar un nuevo cliente
        $('#formClientes').removeClass('collapse'); // Mostrar el formulario
    });

    // Manejo del envío del formulario de creación y modificación
    $('#formClientes form').on('submit', function (e) {
        e.preventDefault(); // Evitar el envío tradicional del formulario

        const cliente_id = $('#editId').val(); // Obtener el ID del cliente a editar
        const clienteData = {
            nombre: $('#nombre').val(),
            apellido1: $('#apellido1').val(),
            apellido2: $('#apellido2').val(),
            correo: $('#correo').val(),
            contrasena: $('#contrasena').val(), // Incluir la contraseña en el POST
        };

        const ajaxSettings = {
            contentType: 'application/json',
            data: JSON.stringify(clienteData),
            error: function (xhr) {
                console.error(cliente_id ? 'Error al actualizar el cliente:' : 'Error al crear el cliente:', xhr.responseText);
                alert(cliente_id ? 'Error al actualizar el cliente. Ver consola para más detalles.' : 'Error al crear el cliente. Ver consola para más detalles.');
            }
        };

        if (cliente_id) { // Si hay un ID, actualiza el cliente
            $.ajax({ ...ajaxSettings, url: `clientes/api/clientes/${cliente_id}`, type: 'PUT' })
                .done(() => {
                    loadClientes(); // Recargar la lista de clientes
                    resetForm(); // Reiniciar el formulario
                    $('#editModal').modal('hide'); // Cerrar el modal de edición
                });
        } else { // Si no hay un ID, crea un nuevo cliente
            $.ajax({ ...ajaxSettings, url: 'clientes/api/clientes', type: 'POST' })
                .done(() => {
                    loadClientes(); // Recargar la lista de clientes
                    resetForm(); // Reiniciar el formulario
                    $('#formClientes').addClass('collapse'); // Ocultar el formulario
                });
        }
    });

    // Manejo del modal de edición
    $('#editModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#editId').val(button.getAttribute('data-id'));
        $('#editNombre').val(button.getAttribute('data-nombre'));
        $('#editApellido1').val(button.getAttribute('data-apellido1'));
        $('#editApellido2').val(button.getAttribute('data-apellido2'));
        $('#editCorreo').val(button.getAttribute('data-correo'));
        $('#newContrasena').val(''); // Inicializar la contraseña
    });

    // Manejo del modal de eliminación
    $('#eliminarModal').on('show.bs.modal', (event) => {
        const button = event.relatedTarget; // Botón que activó el modal
        $('#deleteId').val(button.getAttribute('data-id'));
        $('#deleteNombre').text(button.getAttribute('data-nombre'));
    });

    // Eliminar cliente
    $('#btnEliminar').on('click', function () {
        const clienteId = $('#deleteId').val();
        $.ajax({
            url: `clientes/api/clientes/${clienteId}`,
            type: 'DELETE',
            success: function () {
                loadClientes(); // Recargar la lista de clientes
                $('#eliminarModal').modal('hide'); // Cerrar el modal de eliminación
            },
            error: function (xhr) {
                console.error('Error al eliminar el cliente:', xhr.responseText);
                alert('Error al eliminar el cliente. Ver consola para más detalles.');
            }
        });
    });

    // Función para resetear el formulario
    function resetForm() {
        $('#editId').val('');
        $('#nombre').val('');
        $('#apellido1').val('');
        $('#apellido2').val('');
        $('#correo').val('');
        $('#contrasena').val('');
    }
});
