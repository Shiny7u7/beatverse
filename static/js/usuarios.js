$(document).ready(function () {
    loadUsuarios();

    // Función para cargar los usuarios
    function loadUsuarios() {
        $.get('/usuarios/api/usuarios', function (data) {
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

    // Manejo del formulario de usuarios
    $('#usuarioForm').on('submit', function (e) {
        e.preventDefault();

        const usuario_id = $('#usuario_id').val();
        const usuarioData = {
            nombre: $('#usuario_nombre').val(),
            primerapellido: $('#usuario_primerapellido').val(),
            segundoapellido: $('#usuario_segundoapellido').val(),
            correo: $('#usuario_email').val(),
            contra: $('#usuario_contrasena').val(),
            rol: $('#rolSelect').val()
        };

        const url = usuario_id ? `/usuarios/api/usuarios/${usuario_id}` : `/usuarios/api/usuarios`;
        const method = usuario_id ? 'PUT' : 'POST';

        $.ajax({
            url: url,
            type: method,
            contentType: 'application/json',
            data: JSON.stringify(usuarioData),
            success: function () {
                loadUsuarios();
                resetForm();
            },
            error: function (xhr) {
                console.error('Error:', xhr.responseText);
                alert('Error al guardar los datos del usuario.');
            }
        });
    });

    // Editar usuario
    window.editUsuario = function (id) {
        $.get(`/usuarios/api/usuarios/${id}`, function (data) {
            $('#usuario_id').val(data.usuario_id);
            $('#usuario_nombre').val(data.usuario_nombre);
            $('#usuario_primerapellido').val(data.usuario_primerapellido);
            $('#usuario_segundoapellido').val(data.usuario_segundoapellido);
            $('#usuario_email').val(data.correo);
            $('#usuario_contrasena').val(data.contrasena);
            $('#rolSelect').val(data.rol_id);
            $('#formContainer').removeClass('d-none');
        }).fail(function () {
            alert('Error al cargar los datos del usuario.');
        });
    };

    // Eliminar usuario
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
                    alert('Error al eliminar el usuario.');
                }
            });
        }
    };

    // Resetear el formulario
    function resetForm() {
        $('#usuario_id').val('');
        $('#usuario_nombre').val('');
        $('#usuario_primerapellido').val('');
        $('#usuario_segundoapellido').val('');
        $('#usuario_email').val('');
        $('#usuario_contrasena').val('');
        $('#rolSelect').val('');
        $('#formContainer').addClass('d-none');
    }

    // Botón de cancelar
    $('#btnCancel').on('click', resetForm);
});
