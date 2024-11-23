$(document).ready(function () {
    loadRoles();

    function loadRoles() {
        $.get('/roles/api/roles', function (data) {
            $('#roles-tbody').empty(); // Cambiar a '#roles-tbody' para la tabla de roles
            data.forEach(function (rol) {
                $('#roles-tbody').append(`
                    <tr>
                        <td class="text-center">${rol.rol_id}</td>
                        <td class="text-center">${rol.rol_descripcion}</td>
                        <td class="text-center">
                            <button class='btn btn-warning btn-sm' data-bs-toggle='modal' data-bs-target='#editModal'
                                    data-id='${rol.rol_id}' data-rol='${rol.rol_descripcion}'>
                                Modificar
                            </button>
                            <button class='btn btn-danger btn-sm' data-bs-toggle='modal' data-bs-target='#eliminarModal'
                                    data-id='${rol.rol_id}' data-rol='${rol.rol_descripcion}'>
                                Eliminar
                            </button>
                        </td>
                    </tr>`);
            });
            $('#usuariosTable').removeClass('d-none'); // Cambiar a la ID correspondiente si es necesario
        });
    }

    $('#usuarioForm').on('submit', function (e) {
        e.preventDefault();

        const rolId = $('#id').val(); // Asegúrate de que el campo ID sea parte del formulario
        const rolData = {
            rol: $('#rol').val() // Cambiar según el campo de rol
        };

        if (rolId) {
            $.ajax({
                url: `/roles/api/roles/${rolId}`, // Cambiar a la ruta correspondiente para actualizar
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(rolData),
                success: function () {
                    loadRoles();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al actualizar el rol:', xhr.responseText);
                    alert('Error al actualizar el rol. Ver consola para más detalles.');
                }
            });
        } else {
            $.ajax({
                url: '/roles/api/roles', // Cambiar a la ruta para crear
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(rolData),
                success: function () {
                    loadRoles();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al crear el rol:', xhr.responseText);
                    alert('Error al crear el rol. Ver consola para más detalles.');
                }
            });
        }
    });

    window.deleteRol = function (id) {
        const rol = $('#rolEliminar').val();
        if (confirm(`¿Estás seguro de que deseas eliminar el rol ${rol}?`)) {
            $.ajax({
                url: `/roles/api/roles/${id}`, // Cambiar a la ruta para eliminar
                type: 'DELETE',
                success: function () {
                    loadRoles();
                }
            });
        }
    };

    function resetForm() {
        $('#id').val(''); // Reiniciar ID
        $('#rol').val(''); // Reiniciar campo de rol
        $('#formRoles').collapse('hide'); // Ocultar el formulario
    }

    // Capturar el evento cuando se abre el modal de edición
    var editModal = document.getElementById('editModal');
    editModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // Botón que disparó el modal
        var id = button.getAttribute('data-id');
        var rol = button.getAttribute('data-rol');

        var modalId = editModal.querySelector('#id');
        var modalRol = editModal.querySelector('#rolEdit');

        modalId.value = id;
        modalRol.value = rol;
    });

    // Capturar el evento cuando se abre el modal de eliminación
    var eliminarModal = document.getElementById('eliminarModal');
    eliminarModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // Botón que disparó el modal
        var rol = button.getAttribute('data-rol');
        var id = button.getAttribute('data-id');

        eliminarModal.querySelector('#rolEliminar').innerText = rol; // Mostrar rol a eliminar
        eliminarModal.querySelector('#rolEliminar').value = id; // Guardar ID para eliminar
    });

    $('#btnCancel').on('click', resetForm);
});
