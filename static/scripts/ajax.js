(function (window, document) {
    $(document).ready(function() {
	refreshConsola();
        var refresh = setInterval(refreshConsola, 5000);
	$.ajax({ cache: false });

	//para el estado de Conexion
		var source = new EventSource('/api/sse/state');
		source.onmessage = function (event) {
		 	var msg = JSON.parse(event.data);
		 	
		  	conexion=msg.conectado
		 	console.log("Hola! " + conexion);

		 	if(conexion){
		    	jQuery("#widgetConexion").removeClass("dronDesconectado");
		    	jQuery("#widgetConexion").addClass("dronConectado");
		    	jQuery(".mensajeConectado").css("display", "block");
		    	jQuery(".mensajeDesconectado").css("display", "none");
		 	}
		};
    });

    function refreshConsola(){
	$.ajax({
	    method: 'POST',
	    url: '/api/consolelog',
	    contentType: 'application/json'
	})
	    .done(function(msg){
		var toconsole = msg;
		if (toconsole) {
		    //console.log(toconsole.split("127.0.0.1"))
		    var array = toconsole;
		    var text = '';
		    for (var i in array){
			text += array[i]+"<br>";
		    }
		jQuery("#msgconsola").html(toconsole);
		}
	    });
    }

   
}(this, this.document));

function restartWeb(){
    new Noty({
	type: 'warning',
	layout: 'topRight',
	theme: 'mint',
	text: 'La aplicacion web se esta reiniciando. Este proceso puede demorar unos minutos.',
	timeout: 10000,
	progressBar: true,
	closeWith: ['click', 'button'],
	animation: {
	    open: 'noty_effects_open',
	    close: 'noty_effects_close'
	}
    }).show();
    $.ajax({
	method: 'POST',
	url: '/api/restartweb', error: function(err){
	}
    })
	.done(function(msg){
	});
}

function restartRasp(){
    var n = new Noty({
	text: "<p style='text-align: center;'>Realmente desea reiniciar la raspberry?</p>",
	layout: "topCenter",
	theme: "mint",
	modal: true,
	buttons: [
	    Noty.button('Si', 'pure-button btn-noty-success', function(){
		rebootRasp();
		n.close();
	    }, {id:'button1', 'data-status': 'ok'}),

	    Noty.button('No', 'pure-button btn-noty-error', function(){
		new Noty({
		    type: 'info',
		    layout: 'topRight',
		    theme: 'mint',
		    text: 'A cancelado el reinicio de la raspberry.',
		    timeout: 3000,
		    progressBar: true,
		    closeWith: ['click', 'button'],
		    animation: {
			open: 'noty_effects_open',
			close: 'noty_effects_close'
		    }
		}).show();
		n.close();
	    })
	]
    }).show();
}

function rebootRasp(){
    new Noty({
		    type: 'error',
		    layout: 'topRight',
		    theme: 'mint',
		    text: 'La raspberry se reiniciara en breve. Este proceso puede tardar varios minutos.',
		    timeout: 10000,
		    progressBar: true,
		    closeWith: ['click', 'button'],
		    animation: {
			open: 'noty_effects_open',
			close: 'noty_effects_close'
		    }
		}).show()
    $.ajax({
	method: 'POST',
	url: '/api/restartrasp'
    })
	.done(function(msg){
	});
}

function shutingdownRasp(){
    var n = new Noty({
	text: "<p style='text-align: center;'>Realmente desea apagar la raspberry?</p>",
	layout: "topCenter",
	theme: "mint",
	modal: true,
	buttons: [
	    Noty.button('Si', 'pure-button btn-noty-success', function(){
		shutdownRasp();
		n.close();
	    }, {id:'button1', 'data-status': 'ok'}),

	    Noty.button('No', 'pure-button btn-noty-error', function(){
		new Noty({
		    type: 'info',
		    layout: 'topRight',
		    theme: 'mint',
		    text: 'El apagado de la raspberry a sido cancelado.',
		    timeout: 3000,
		    progressBar: true,
		    closeWith: ['click', 'button'],
		    animation: {
			open: 'noty_effects_open',
			close: 'noty_effects_close'
		    }
		}).show();
		n.close();
	    })
	]
    }).show();
}

function shutdownRasp(){
    new Noty({
	type: 'error',
	layout: 'topRight',
	theme: 'mint',
	text: 'La raspberry se apagara en 1 minuto.',
	timeout: 8000,
	progressBar: true,
	closeWith: ['click', 'button'],
	animation: {
	    open: 'noty_effects_open',
	    close: 'noty_effects_close'
	}
    }).show()
    $.ajax({
	method: 'POST',
	url: '/api/shutdownrasp'
    })
	.done(function(msg){
	});
}

function descargarLogs(){
    window.location.href = '/api/descargarlogs'
}
function descargarBD(){
    window.location.href = '/api/descargarbd'
}

function confirmacionBorrarFotos(){
	var n = new Noty({
	text: "<p style='text-align: center;'>Realmente desea borrar todas las fotos almacenadas? No se podrán recuperar</p>",
	layout: "topCenter",
	theme: "mint",
	modal: true,
	buttons: [
	    Noty.button('Si', 'pure-button btn-noty-success', function(){
		borrarTodasLasFotos();
		n.close();
	    }, {id:'button1', 'data-status': 'ok'}),

	    Noty.button('No', 'pure-button btn-noty-error', function(){
		
		n.close();
	    })
	]
    }).show();
}

function borrarTodasLasFotos(){
	console.log("borra");

	var inst = $('[data-remodal-id=modal]').remodal();

	inst.open();

	$.ajax({
	    method: 'GET',
	    url: '/api/borrarfotos/0',
	    contentType : 'application/json',
	    error: function(data){
	  		inst.close();
        }
	  })
  	.done(function( msg ) {
	  	inst.close();
	  	console.log("Mensaje: " + JSON.stringify(msg));
	  	console.log(msg['nombre']);
	  	if(msg['ok'] == true){
	  		new Noty({
				type: 'success',
				layout: 'topRight',
				theme: 'mint',
				text: 'Se borraron todas las fotos de la raspberry',
				timeout: 10000,
				progressBar: true,
				closeWith: ['click', 'button'],
				animation: {
				    open: 'noty_effects_open',
				    close: 'noty_effects_close'
				}
		    }).show();
		    
	  	} else {
	  		new Noty({
				type: 'warning',
				layout: 'topRight',
				theme: 'mint',
				text: 'Hubo un error al borrar las fotos: ' + msg['nombre'] ,
				timeout: 10000,
				progressBar: true,
				closeWith: ['click', 'button'],
				animation: {
				    open: 'noty_effects_open',
				    close: 'noty_effects_close'
				}
		    }).show();
			    
	  	}
	});
}

function confirmacionlimpiarBD() {
	var n = new Noty({
	text: "<p style='text-align: center;'>Realmente desea borrar todos los registros de la Base de Datos? No se podrán recuperar</p>",
	layout: "topCenter",
	theme: "mint",
	modal: true,
	buttons: [
	    Noty.button('Si', 'pure-button btn-noty-success', function(){
		limpiarBaseDeDatos();
		n.close();
	    }, {id:'button1', 'data-status': 'ok'}),

	    Noty.button('No', 'pure-button btn-noty-error', function(){
		
		n.close();
	    })
	]
    }).show();
}

function exportarDB(){
	console.log("exportarbd");
	var inst = $('[data-remodal-id=modal]').remodal();

	//inst.open();
	$.ajax({
	    method: 'POST',
	    url: '/api/exportarbd',
	    contentType : 'application/json',
	    error: function(data){
	  		//inst.close();
        }
	  })
  	.done(function( msg ) {
	  	//inst.close();
	  	console.log("Mensaje: " + JSON.stringify(msg));
	  	if(msg['ok'] == true){
	  		new Noty({
				type: 'success',
				layout: 'topRight',
				theme: 'mint',
				text: 'Las base de datos se descargara en breve',
				timeout: 10000,
				progressBar: true,
				closeWith: ['click', 'button'],
				animation: {
				    open: 'noty_effects_open',
				    close: 'noty_effects_close'
				}
			}).show();
		    descargarBD();
		    
	  	} else {
	  		new Noty({
				type: 'warning',
				layout: 'topRight',
				theme: 'mint',
				text: 'Hubo un error al exportar la base de datos: ' + msg['nombre'] ,
				timeout: 10000,
				progressBar: true,
				closeWith: ['click', 'button'],
				animation: {
				    open: 'noty_effects_open',
				    close: 'noty_effects_close'
				}
		    }).show();
			    
	  	}
	});
}

function limpiarBaseDeDatos(){
    console.log("borro");
    new Noty({
				type: 'success',
				layout: 'topRight',
				theme: 'mint',
				text: 'Espere mientras se borra la base de datos, los servicios se reiniciaran',
				timeout: 10000,
				progressBar: true,
				closeWith: ['click', 'button'],
				animation: {
				    open: 'noty_effects_open',
				    close: 'noty_effects_close'
				}
			}).show();
    $.ajax({
	    method: 'POST',
	    url: '/api/limpiarbd',
	    contentType : 'application/json',
	    error: function(data){
	  		//inst.close();
	    console.log("doneerror");
        }
	  })
  	.done(function( msg ) {
	    console.log("done");
	});
}

