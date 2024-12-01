
document.getElementById('registroFormulario').addEventListener('submit', function(event) {
    event.preventDefault();

    var email = document.getElementById('email').value;
    var contraseña = document.getElementById('contraseña').value;
    var confirmarContraseña = document.getElementById('confirmarContraseña').value;


    if (contraseña !== confirmarContraseña) { // vefica que las contraseñas sean iguales
    alert('Las contraseñas no coinciden');
    return;
    }

    console.log('Registro exitoso', { // aca agregar el correo a la base de datso
        email: email,
        contraseña: contraseña
    });
}); 