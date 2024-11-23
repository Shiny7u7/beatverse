//js/usuarios.js

$(document).ready(function () { 
    loadUsuarios();

    function loadUsuarios() {
        $.get('/usuarios/api/usuarios', function (data) {  // Cambio aquí
            $('#usuarios-tbody').empty();
            data.forEach(function (usuario) {
                $('#usuarios-tbody').append(`
                    <tr>
                        <td class="text-center">${usuario.usuario_nombre}</td>
                        <td class="text-center">${usuario.usuario_primerapellido}</td>
                        <td class="text-center">${usuario.usuario_segundoapellido}</td>
                        <td class="text-center">${usuario.rol_descripcion}</td>
                        <td class="text-center">${usuario.estado_descripcion}</td>
                        <td class="text-center">
                            <button class='btn btn-warning btn-sm' onclick='editUsuario(${usuario.usuario_id})'>Modificar</button>
                            <button class='btn btn-danger btn-sm' onclick='deleteUsuario(${usuario.usuario_id})'>Eliminar</button>
                        </td>
                    </tr>`);
            });
            $('#usuariosTable').removeClass('d-none');
        });
    }

    $('#btnAddUsuario').on('click', function () {
        resetForm(); 
        $('#formContainer').removeClass('d-none'); 
    });

    $('#usuarioForm').on('submit', function (e) {
        e.preventDefault(); 
        
        const usuario_id = $('#usuario_id').val();
        const usuarioData = {
            usuario_nombre: $('#usuario_nombre').val(),
            usuario_primerapellido: $('#usuario_primerapellido').val(),
            usuario_segundoapellido: $('#usuario_segundoapellido').val(),
            rol_id: $('#rolSelect').val()  // Aquí suponiendo que el rol es el ID del rol seleccionado
        };

        if (usuario_id) {
            $.ajax({
                url: `/usuarios/api/usuarios/${usuario_id}`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(usuarioData),
                success: function () {
                    loadUsuarios();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al actualizar el usuario:', xhr.responseText);
                    alert('Error al actualizar el usuario. Ver consola para más detalles.');
                }
            });
        } else {
            $.ajax({
                url: `/usuarios/api/usuarios/`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(usuarioData),
                success: function () {
                    loadUsuarios();
                    resetForm();
                },
                error: function (xhr) {
                    console.error('Error al crear el usuario:', xhr.responseText);
                    alert('Error al crear el usuario. Ver consola para más detalles.');
                }
            });
        }
    });

    window.editUsuario = function (id) {
        $.get(`/usuarios/api/usuarios/${id}`, function (data) {
            // Cambio aquí
            $('#usuario_id').val(data.usuario_id);
            $('#usuario_nombre').val(data.usuario_nombre);
            $('#usuario_primerapellido').val(data.primerapellido);
            $('#usuario_segundoapellido').val(data.segundoapellido);
            $('#usuario_email').val(data.correo);
            $('#usuario_contrasena').val(data.contrasena);
            $('#rolSelect').val(data.rol_id);
            $('#formContainer').removeClass('d-none'); 
        }).fail(function () {
            alert('Error al cargar los datos del usuario.');
        });
    };

    window.deleteUsuario = function (id) {
        if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
            $.ajax({
                url: `/usuarios/api/usuarios/${id}`,
                type: 'DELETE',
                success: function () {
                    loadUsuarios();
                },
                error: function (xhr) {
                    console.error('Error al eliminar el usuario:', xhr.responseText);
                    alert('Error al eliminar el usuario. Ver consola para más detalles.');
                }
            });
        }
    };

    function resetForm() {
        $('#usuario_id').val('');
        $('#usuario_nombre').val('');
        $('#usuario_primerapellido').val('');
        $('#usuario_segundoapellido').val('');
        $('#rolSelect').val('');
        $('#formContainer').addClass('d-none'); 
    }

    $('#btnCancel').on('click', resetForm);
});
