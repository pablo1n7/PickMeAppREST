function enviar(_nombre,_latlng,_descripcion,_usuario) {
    console.log("envio listo");
    var lugar = {};
    lugar.nombre = _nombre;
    lugar.latlng = _latlng;
    lugar.descripcion = _descripcion;
    lugar.usuario = _usuario;

    $.ajax({
        url: '/guardarlugar',
        contentType: 'application/json',
        dataType : 'json',
        data: JSON.stringify(lugar),
        type: 'POST',
        success: function(response) {
            console.log(response);
            //var notification = alertify.notify('Robot registrado con exito!', 'success', 10, function(){  location.reload() });
        },
        error: function(error) {
            //var notification = alertify.notify('Ups ocurrio un error', 'error', 10, function(){  console.log('dismissed'); });
        }
    });   
}

function crear_usuario(_nombre,_id) {
    console.log("envio listo");
    var usuario = {};
    usuario.nombre = _nombre;
    usuario.id_usuario = _id;

    $.ajax({
        url: '/guardarusuario',
        contentType: 'application/json',
        dataType : 'json',
        data: JSON.stringify(usuario),
        type: 'POST',
        success: function(response) {
            console.log(response);
            //var notification = alertify.notify('Robot registrado con exito!', 'success', 10, function(){  location.reload() });
        },
        error: function(error) {
            //var notification = alertify.notify('Ups ocurrio un error', 'error', 10, function(){  console.log('dismissed'); });
        }
    });   
}