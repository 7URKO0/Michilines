
document.getElementById('inicioSesionFormulario').addEventListener('submit', function(event) {
    event.preventDefault();

    var email = document.getElementById('email').value;
    var contraseña = document.getElementById('contraseña').value;
    
    console.log('Email:', email);
    console.log('Contraseña:', contraseña);
}); 