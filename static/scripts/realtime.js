// Create an image layer
var FUDGE = 0.0005;
var OFFSETX = 0.0001;
var OFFSETY = -0.0002;
var conexion=false
//var armado=False
var arm=false;
var coordenadas=[];
var contcoord=0;
var recorridos=[];
var contrec=0;
var xrel=0;
var yrel=0;
var entreCombo=false;

function mal(dato){
    //console.log("mi dato" + dato);
    return isNaN(parseInt(dato))
}

$('#header-arm').on('click', function () {
  var armenv=1;
  //si esta armado hay que desarmar
  if (arm==true) armenv=0;
  if (!conexion){
	new Noty({
	    type: 'error',
	    layout: 'topRight',
	    theme: 'mint',
	    text: 'No se encuentra conectado',
	    timeout: 5000,
	    progressBar: true,
	    closeWith: ['click', 'button'],
	    animation: {
		open: 'noty_effects_open',
		close: 'noty_effects_close'
	    },
		}).show()
	return;
  }

  $.ajax({
    method: 'PUT',
    url: '/api/arm',
    contentType : 'application/json',
    data: JSON.stringify({ arm: armenv }),
  })
  .done(function( msg ) {
    console.log('Enviado mensaje de armado/desarmado')
  });
})

$('#header-ini-mision').on('click', function () {
  if (!conexion){
	new Noty({
	    type: 'error',
	    layout: 'topRight',
	    theme: 'mint',
	    text: 'No se encuentra conectado',
	    timeout: 5000,
	    progressBar: true,
	    closeWith: ['click', 'button'],
	    animation: {
		open: 'noty_effects_open',
		close: 'noty_effects_close'
	    },
		}).show()
	return;
  }
  var resolucion=$("#resolucion").val();
  var umbral=$("#umbral").val();
  var demora=$("#demora").val();
  var movfotos=$("#movfotos").val();
  var altitud=$("#altitud").val();
  var v=$("#vel").val() ;
  var h=$("#alt").val();
  if (mal(v) || mal(h)){
  	new Noty({
	    type: 'error',
	    layout: 'topRight',
	    theme: 'mint',
	    text: 'Debe ingresar 2 valores numericos válidos para la altura y la valocidad',
	    timeout: 5000,
	    progressBar: true,
	    closeWith: ['click', 'button'],
	    animation: {
		open: 'noty_effects_open',
		close: 'noty_effects_close'
	    },
		}).show();
	
	}
  else
	{
		new Noty({
		    type: 'success',
		    layout: 'topRight',
		    theme: 'mint',
		    text: 'La misión ha iniciado',
		    timeout: 5000,
		    progressBar: true,
		    closeWith: ['click', 'button'],
		    animation: {
			open: 'noty_effects_open',
			close: 'noty_effects_close'
		    },
			}).show();


	  $.ajax({
	    method: 'PUT',
	    url: '/api/iniciarmision',
	    contentType : 'application/json',
	    data: JSON.stringify({ umbral:umbral, resolucion:resolucion, demora:demora, movfotos:movfotos, altitud:altitud}),
	  })
	  .done(function( msg ) {
	    if (msg.ok==false){
    		new Noty({
			    type: 'error',
			    layout: 'topRight',
			    theme: 'mint',
			    text: 'No fue posible completar la misión. Verifique haber ingresado coordenadas',
			    timeout: 5000,
			    progressBar: true,
			    closeWith: ['click', 'button'],
			    animation: {
				open: 'noty_effects_open',
				close: 'noty_effects_close'
			    },
				}).show();
	  		} else {
	  			new Noty({
				    type: 'success',
				    layout: 'topRight',
				    theme: 'mint',
				    text: 'Misión finalizada',
				    timeout: 5000,
				    progressBar: true,
				    closeWith: ['click', 'button'],
				    animation: {
					open: 'noty_effects_open',
					close: 'noty_effects_close'
				    },
					}).show();
	  		}
	  });
	}
})

$('#header-despegar').on('click', function () {
  if (!conexion){
	new Noty({
	    type: 'error',
	    layout: 'topRight',
	    theme: 'mint',
	    text: 'No se encuentra conectado',
	    timeout: 5000,
	    progressBar: true,
	    closeWith: ['click', 'button'],
	    animation: {
		open: 'noty_effects_open',
		close: 'noty_effects_close'
	    },
		}).show()
	return;
  }

  var v=$("#vel").val();
  var h=$("#alt").val();
  if (mal(v) || mal(h)){
	new Noty({
	    type: 'error',
	    layout: 'topRight',
	    theme: 'mint',
	    text: 'Para ingresar una coordenada debe ingresar 2 valores numericos válidos para la altura y la velocidad',
	    timeout: 5000,
	    progressBar: true,
	    closeWith: ['click', 'button'],
	    animation: {
		open: 'noty_effects_open',
		close: 'noty_effects_close'
	    },
		}).show();
	}
  else
	{
	  $.ajax({
	    method: 'PUT',
	    url: '/api/despegar',
	    contentType : 'application/json',
	    data: JSON.stringify({ altura:h, velocidad:v }),
	  })
	  .done(function( msg ) {
			new Noty({
			    type: 'success',
			    layout: 'topRight',
			    theme: 'mint',
			    text: 'Mision finalizada',
			    timeout: 5000,
			    progressBar: true,
			    closeWith: ['click', 'button'],
			    animation: {
				open: 'noty_effects_open',
				close: 'noty_effects_close'
			    },
				}).show();
	  });
	}
})


$('#header-mover').on('click', function () {
  $.ajax({
    method: 'POST',
    url: '/api/mover',
    contentType : 'application/json',
    data: JSON.stringify({ direccion:1 }),
  })
  .done(function( msg ) {
    console.log('Pa mover uno')
  });
})


$('#header-flotar').on('click', function () {
  var v=$("#vel").val();
  var h=$("#alt").val();
  if (mal(v) || mal(h)){
	new Noty({
	    type: 'error',
	    layout: 'topRight',
	    theme: 'mint',
	    text: 'Para ingresar una coordenada debe ingresar 2 valores numericos válidos para la altura y la valocidad',
	    timeout: 5000,
	    progressBar: true,
	    closeWith: ['click', 'button'],
	    animation: {
		open: 'noty_effects_open',
		close: 'noty_effects_close'
	    },
		}).show();
	}
  else
	{
	  $.ajax({
	    method: 'PUT',
	    url: '/api/flotar',
	    contentType : 'application/json',
	    data: JSON.stringify({ altura:h, velocidad:v }),
	  })
	  .done(function( msg ) {
	    console.log('Queda flotando')
	  });
	}
})


/*$('#header-figura').on('click', function () {
  var d=$("#met").val();
  var h=$("#alt").val();
  if (mal(d) || mal(h)){
	alert("Para ingresar una coordenada debe ingresar 2 valores numericos válidos para la altura y la distancia");
	}
  else
	{
	$.ajax({
	    method: 'PUT',
	    url: '/api/genFigura',
	    contentType : 'application/json',
	    data: JSON.stringify({ altura:h, metros:d }),
	  })
	  .done(function( msg ) {
	    alert(msg.coord);
	    console.log('Figurita generada')
	  });
	}
})*/


$('#header-una-foto').on('click', function () {
  $.ajax({
    method: 'PUT',
    url: '/api/unafoto',
    contentType : 'application/json',
  })
  .done(function( msg ) {
    new Noty({
	    type: 'success',
	    layout: 'topRight',
	    theme: 'mint',
	    text: 'Se sacó una foto',
	    timeout: 5000,
	    progressBar: true,
	    closeWith: ['click', 'button'],
	    animation: {
		open: 'noty_effects_open',
		close: 'noty_effects_close'
	    },
		}).show();
  });
})


/*COORDENADAS */

function mostrarTipoRec(tipor){
	if (tipor==0){
		return "Estacas"
	}else {
		return "Mapping"
	}
}

function mostrarTipoAI(tipo){
	if (tipo==0){
		return "Estaca"
	}else {
		return "Común"
	}
}

$('#selrec').on('mouseleave', function () {
    console.log("Me fui");
    entreCombo=false;
});

$('#selrec').on('mouseenter', function () {
    console.log("llegue");
    entreCombo=true;
});

$('.aControlar').on('change', function () {
	//console.log("cambiooooo");
	//console.log("Valor original: " + jQuery(this).attr("data-original") + " actual: " + jQuery(this).val());
	if(jQuery(this).attr("data-original") != jQuery(this).val()){
		jQuery(this).css('background-color', '#ddeaff');
		jQuery(this).css('border', '1px solid rgb(66, 184, 221)');
		new Noty({
			type: 'info',
			layout: 'topRight',
			theme: 'mint',
			text: 'Los cambios que haga se mantendrán durante la misión',
			timeout: 7000,
			progressBar: true,
			closeWith: ['click', 'button'],
			animation: {
			    open: 'noty_effects_open',
			    close: 'noty_effects_close'
			}
	    }).show();
	} else {
		jQuery(this).css('background-color', 'white');
		jQuery(this).css('border', '1px solid gray');
	}
});


$('#selrec').on('change', function () {
  //alert("recorrido dado de alta");
  var recsel=$("#selrec").val();
  //var umbral=$("#umbral").val();
  //var resolucion=$("#resolucion").val();
  if (recsel==0){
	//Vaciar los puntos a mostrar
    $("#padron").val("");
    $("#alt").val("");
    $("#vel").val("");
    $("#tipo").val("");
    //$("#puntosrec").html("<tr><td>id</td><td>x</td><td>y</td><td>h</td><td>tipo</td></tr>");
	}
  else
	{
	$.ajax({
		method: 'PUT',
		url: '/api/datosrecorrido',
		contentType : 'application/json',
		data: JSON.stringify({ recorrido: recsel}),
	})
	.done(function( msg ) {
		if (msg.ok) {
			//alert(msg)
			$("#padron").val(msg.recorrido.padron);
			$("#padron").attr("data-original", msg.recorrido.padron);
			$("#alt").val(msg.recorrido.alt);
			$("#alt").attr("data-original", msg.recorrido.alt);
			$("#vel").val(msg.recorrido.vel);
			$("#vel").attr("data-original", msg.recorrido.vel);
			$("#cantpuntos").val(msg.recorrido.cantpuntos);
			$("#cantpuntos").attr("data-original", msg.recorrido.cantpuntos);
			$("#calculodist").val(msg.recorrido.calculodist);
			$("#calculodist").attr("data-original", msg.recorrido.calculodist);
			if (msg.recorrido.umbral==0){
			    $("#umbral").val(0.5);
			    $("#umbral").attr("data-original", 0.5);
		    }
			else{
			    $("#umbral").val(msg.recorrido.umbral*2);
			    $("#umbral").attr("data-original", msg.recorrido.umbral*2);
			}

			$("#tipo").val(mostrarTipoRec(msg.recorrido.tipo));
			$("#tipo").attr("data-original", msg.recorrido.tipo);
			//$("#puntosrec").html("<tr><td>id</td><td>x</td><td>y</td><td>h</td><td>tipo</td></tr>");
			$.each( msg.puntos, function( key, punto ) {
			  	//alert( key + ": " + value );
			  	$("#puntosrec").append("<tr><td>"+punto.id+"</td><td>"+punto.x+"</td><td>"+punto.y+"</td><td>"+punto.h+"</td><td>"+mostrarTipoAI(punto.tipo)+"</td></tr>");
			  });

			console.log('RECORRIDO LEIDO')
		}else{
			new Noty({
			    type: 'error',
			    layout: 'topRight',
			    theme: 'mint',
			    text: 'No fue posible seleccionar el recorrido',
			    timeout: 5000,
			    progressBar: true,
			    closeWith: ['click', 'button'],
			    animation: {
				open: 'noty_effects_open',
				close: 'noty_effects_close'
			    },
				}).show();
		}
	});
	}
})

$('#guardar-recorrido').on('click', function () {
  console.log(coordenadas);
  if(!ordenarCoordenadas()){
  	return;
  }
  console.log(coordenadas);
  //fata controlar
 // return false;
  //alert("recorrido dado de alta");
  var p=$("#padron").val();
  var a=$("#alt").val();
  var v=$("#vel").val();
  var t=$("#tipo").val();
  var c=$("#cantpuntos").val();
  var sol=$("#solapamiento").val();
  var dist=$("#dist").val();
  var umbral=$("#umbral").val();
  var rel=$("#relativas").is(":checked");
  if (mal(p) || mal(a) || mal(v)){
	new Noty({
		    type: 'error',
		    layout: 'topRight',
		    theme: 'mint',
		    text: 'Para dar de alta el recorrido debe ingresar 3 valores numericos válidos para el padrón, la altura y la velocidad',
		    timeout: 5000,
		    progressBar: true,
		    closeWith: ['click', 'button'],
		    animation: {
			open: 'noty_effects_open',
			close: 'noty_effects_close'
		    },
			}).show();
	}
  else
	{
	if (contcoord<=0){
		new Noty({
		    type: 'error',
		    layout: 'topRight',
		    theme: 'mint',
		    text: 'Debe ingresar al menos un punto para poder dar de alta un recorrido nuevo',
		    timeout: 5000,
		    progressBar: true,
		    closeWith: ['click', 'button'],
		    animation: {
			open: 'noty_effects_open',
			close: 'noty_effects_close'
		    },
			}).show();
	}else{

	    //Agregamos una área de Interes 0,0 para que vuelva siempre para el inicio
	    //var nuevac = {x: 0, y: 0, h: coordenadas[contcoord-1].h,tipo:1}
	    //coordenadas[contcoord]=nuevac;
	    //MAS FACIL HACER ESTO DESDE LA LOGICA NOMAS

		$.ajax({
			method: 'PUT',
			url: '/api/guardarrecorrido',
			contentType : 'application/json',
			data: JSON.stringify({ padron: p, alt: a, vel: v, tipo: t, coordenadas:coordenadas, rel:rel, xrel:xrel, yrel:yrel, cantpuntos:c, dist:dist, umbral:umbral, sol:sol}),
		})
		.done(function( msg ) {
			//alert("Coordenada guardada");
			//console.log('enviada la coordenada')
			if (msg.ok) {
				$("#padron").val("");
				$("#alt").val("");
				$("#vel").val("");
				$("#relativas").prop("checked",true);

				//Eliminar todas las coordenadas. Lo comentamos para permitir el ingreso de mas de un recorrido con distintas config pero mismas coordenadas
				/*coordenadas.splice(0,contcoord);
				contcoord=0;
				$("#puntosrec").html("<tr><td>x</td><td>y</td><td>h</td><td>tipo</td></tr>");*/

				new Noty({
				    type: 'success',
				    layout: 'topRight',
				    theme: 'mint',
	  			    text: 'Recorrido Guardado',
				    timeout: 5000,
				    progressBar: true,
				    closeWith: ['click', 'button'],
				    animation: {
					open: 'noty_effects_open',
					close: 'noty_effects_close'
				    },
  				}).show();
			}else{	
				new Noty({
				    type: 'error',
				    layout: 'topRight',
				    theme: 'mint',
	  			    text: 'No se pudo dar de alta el recorrido',
				    timeout: 5000,
				    progressBar: true,
				    closeWith: ['click', 'button'],
				    animation: {
					open: 'noty_effects_open',
					close: 'noty_effects_close'
				    },
  				}).show()
			}
		});
		}
	}
})

$('#header-del-mision').on('click', function () {
  //coordenadas[contcoord]=[];
  coordenadas.splice(0,contcoord);
  contcoord=0;
  //$("#puntosrec").html("<tr><td>x</td><td>y</td><td>h</td><td>tipo</td></tr>");
  if(typeof limpiarMapa === "function"){
  	limpiarMapa();
  }
})

$('#header-add-coordenada').on('click', function () {
  var x=$("#x").val();
  var y=$("#y").val();
  var h=$("#h").val();
  var tipop=$("#tipop").val();
  //var rel=$("#relativas").is(":checked");
  var xr=$("#xrel").val();
  var yr=$("#yrel").val();
  var nombre = $("#nombrePunto").val();
  if (mal(x) || mal(y) || mal(h)){
	new Noty({
	    type: 'error',
	    layout: 'topRight',
	    theme: 'mint',
	    text: 'Para ingresar una coordenada debe ingresar 3 valores numericos válidos para la altura, x e y',
	    timeout: 5000,
	    progressBar: true,
	    closeWith: ['click', 'button'],
	    animation: {
		open: 'noty_effects_open',
		close: 'noty_effects_close'
	    },
		}).show()
	}
  else
	{
	//Si estamos poniendo coordenadas absolutas hay que revisar que hayan puesto la primera relativa
	/*if (!rel && (contcoord<1)){
	    if (mal(xr) || mal(yr)){
	        new Noty({
			    type: 'error',
			    layout: 'topRight',
			    theme: 'mint',
			    text: 'Debe ingresar 2 valores numericos válidos para las coordenadas relativas solicitadas',
			    timeout: 5000,
			    progressBar: true,
			    closeWith: ['click', 'button'],
			    animation: {
				open: 'noty_effects_open',
				close: 'noty_effects_close'
			    },
				}).show();
	        return false;
	    }else{
	        xrel=xr;
	        yrel=yr;
	        //ocultamos las opciones de absolutas porque solo la primera se ingresa la relativa
	        $("#opcionesabsolutas").hide();
	    }
	}*/
	//Agregamos las coordenadas de mantera local
  if(agregarPunto()){
      var nuevac = {
            nombre: nombre,
            x: x,
            y: y,
            h: h,
            tipo:tipop
      }
      coordenadas[contcoord]=nuevac;

       //$("#puntosrec").append("<tr><td>"+x+"</td><td>"+y+"</td><td>"+h+"</td><td>"+mostrarTipoAI(tipop)+"</td></tr>");
         
      //alert("Coordenada agregada "+JSON.stringify(coordenadas));
       new Noty({
			    type: 'success',
			    layout: 'topRight',
			    theme: 'mint',
			    text: 'Se agregó la coordenada',
			    timeout: 5000,
			    progressBar: true,
			    closeWith: ['click', 'button'],
			    animation: {
				open: 'noty_effects_open',
				close: 'noty_effects_close'
			    },
				}).show();
      contcoord++;
  } 
	
	}
})


$('#header-fecha').on('click', function () {
    //cambiar el mes por el año
    var fechatxt=$("#fecha").val();
    var res=fechatxt.split(" ");
    var dmy=res[0];
    var hora=res[1];
    var resdmy=dmy.split("/");
    //var reshora=hora.split(":");
    var fecha=resdmy[1]+"/"+resdmy[0]+"/"+resdmy[2]+" "+hora;
    //alert(resdmy);
    //alert(reshora);
    //var fecha=new Date(parseInt(resdmy[2]),parseInt(resdmy[1])-1,parseInt(resdmy[0]),parseInt(reshora[0]),parseInt(reshora[1]),parseInt(reshora[2]),0);
    //alert(fecha);
    //alert(dmy);
    //alert(hora);
    $.ajax({
        method: 'POST',
        url: '/api/cambiarfecha',
        contentType : 'application/json',
        data:  JSON.stringify({ fecha: fecha})
    }).done(function( msg ) {
        if (msg.ok) alert("Fecha del sistema cambiada con exito");
        else alert("No fue posible cambiar la fecha");
        console.log('se cambio la fecha? ' + msg.ok)
    });
})



$('#header-conectar-desconectar').on('click', function () {
    var sim=$("#simular").is(":checked");
    //alert(sim);
    console.log('Entrando al ajax');
    if ($('#header-conectar-desconectar').hasClass('button-success')){
	$('#header-conectar-desconectar').addClass('pure-button-disabled');
	$('#iconocargando').show();
	$('#conect-desc-span').hide();
	$.ajax({
	    method: 'PUT',
	    url: '/api/conectar',
	    contentType : 'application/json',
	    data: JSON.stringify({ cadena: 'tcp:192.168.1.45:5760', sim:sim }),
	    //data: JSON.stringify({ cadena: 'udp:127.0.0.1:14550' })
	    //data: JSON.stringify({ cadena: $("#cadena").val(), sim:sim })
	})
	    .done(function( msg ) {
		if (msg.ok) {
		    new Noty({
			type: 'success',
			layout: 'topRight',
			theme: 'mint',
	  		text: 'Conectado exitosamente',
			timeout: 5000,
			progressBar: true,
			closeWith: ['click', 'button'],
			animation: {
			    open: 'noty_effects_open',
			    close: 'noty_effects_close'
			},
  		    }).show()
		    $('#header-conectar-desconectar').removeClass('button-success');
		    $('#header-conectar-desconectar').removeClass('pure-button-disabled');
		    $('#header-conectar-desconectar').addClass('button-error');
		    $('#conect-desc-span').text('Desconectar');
		    $('#iconocargando').hide();
		    $('#conect-desc-span').show();
		    conexion=true
		    $("#selrec").val(0).change();
		}
		else new Noty({
		    type: 'error',
		    layout: 'topRight',
		    theme: 'mint',
  		    text: 'No fue posible conectarse',
		    timeout: 5000,
		    progressBar: true,
		    closeWith: ['click', 'button'],
		    animation: {
			open: 'noty_effects_open',
			close: 'noty_effects_close'
		    },
		}).show()
		$('#header-conectar-desconectar').removeClass('pure-button-disabled');
		$('#iconocargando').hide();
		$('#conect-desc-span').show();
		console.log('se conectó? ' + msg.ok)
	    });
    }
    if ($('#header-conectar-desconectar').hasClass('button-error')){
	$('#header-conectar-desconectar').addClass('pure-button-disabled');
	$('#iconocargando').show();
	$('#conect-desc-span').hide();
	$.ajax({
	    method: 'PUT',
	    url: '/api/desconectar',
	    contentType : 'application/json'
	})
	    .done(function( msg ) {
		if (msg.ok) {
		    new Noty({
			type: 'warning',
			layout: 'topRight',
			theme: 'mint',
	  		text: 'Desconectado exitosamente',
			timeout: 5000,
			progressBar: true,
			closeWith: ['click', 'button'],
			animation: {
			    open: 'noty_effects_open',
			    close: 'noty_effects_close'
			},
  		    }).show()
		    $('#header-conectar-desconectar').removeClass('button-error');
		    $('#header-conectar-desconectar').removeClass('pure-button-disabled');
		    $('#header-conectar-desconectar').addClass('button-success');
		    $('#conect-desc-span').text('Conectar');
		    $('#iconocargando').hide();
		    $('#conect-desc-span').show();
		    conexion=false
		    $("#selrec").val(0).change();
		}
		else new Noty({
		    type: 'error',
		    layout: 'topRight',
		    theme: 'mint',
  		    text: 'No fue posible desconectarse',
		    timeout: 5000,
		    progressBar: true,
		    closeWith: ['click', 'button'],
		    animation: {
			open: 'noty_effects_open',
			close: 'noty_effects_close'
		    },
  		}).show()
		$('#header-conectar-desconectar').removeClass('pure-button-disabled');
		$('#iconocargando').hide();
		$('#conect-desc-span').show();
		console.log('se desconectó? ' + msg.ok)
	    });
    }
})


$('#relativas').on('click', function () {
    //SOLO MOSTRAMOS LA PRIMERA VEZ LAS OPCIONES PARA ABSOLUTAS
    if ($("#relativas").is(":checked") || (contcoord>=1)){
        $("#opcionesabsolutas").hide();
    }else{
        $("#opcionesabsolutas").show();
    }
})

/*$('#primerestaca').on('click', function () {
    if ($("#primerestaca").is(":checked")){
        $("#posrelativa").show();
    }else{
        $("#posrelativa").hide();
    }
})*/


/*
$('#header-desconectar').on('click', function () {
    if ($('#header-desconectar').hasClass('button-error')){
	$('#header-desconectar').addClass('pure-button-disabled');
	$('#iconocargando').show();
	$('#desc-span').hide();
    }
    $.ajax({
	method: 'PUT',
	url: '/api/desconectar',
	contentType : 'application/json'
    })
	.done(function( msg ) {
	    if (msg.ok) {
		new Noty({
		    type: 'warning',
		    layout: 'topRight',
		    theme: 'mint',
	  	    text: 'Desconectado exitosamente',
		    timeout: 5000,
		    progressBar: true,
		    closeWith: ['click', 'button'],
		    animation: {
			open: 'noty_effects_open',
			close: 'noty_effects_close'
		    },
  		}).show()
		$('#header-desconectar').removeClass('button-error');
		$('#header-desconectar').removeClass('pure-button-disabled');
		$('#header-desconectar').addClass('button-success');
		$('#conectar-span').swap('#desc-span');
		$('#iconocargando').hide();
		$('#conectar-span').show();
		var boton = document.getElementById('header-desconectar');
		boton.id = "header-conectar";
		conexion=false
		$("#selrec").val(0).change();
	    }
	    else new Noty({
		type: 'error',
		layout: 'topRight',
		theme: 'mint',
  		text: 'No fue posible desconectarse',
		timeout: 5000,
		progressBar: true,
		closeWith: ['click', 'button'],
		animation: {
		    open: 'noty_effects_open',
		    close: 'noty_effects_close'
		},
  	    }).show()
	    $('#header-desconectar').removeClass('pure-button-disabled');
	    $('#iconocargando').hide();
	    $('#desc-span').show();
	    console.log('se desconectó? ' + msg.ok)
	});
})*/


$('#header-fin-mision').on('click', function () {
  $.ajax({
    method: 'PUT',
    url: '/api/mode',
    contentType : 'application/json',
    data: JSON.stringify({ mode: 'RTL' }),
  })
  .done(function( msg ) {
    console.log('sent mode change')
  });
})

$('#header-mode-land').on('click', function () {
  $.ajax({
    method: 'PUT',
    url: '/api/mode',
    contentType : 'application/json',
    data: JSON.stringify({ mode: 'LAND' }),
  })
  .done(function( msg ) {
    console.log('sent mode change')
  });
})


var hoy=new Date();
//alert(fechaactual);
$('#fecha').val(hoy.getDate()+"/"+(hoy.getMonth()+1)+"/"+hoy.getFullYear()+" "+hoy.getHours()+":"+hoy.getMinutes()+":"+hoy.getSeconds());

var globmsg = null;

var source = new EventSource('/api/sse/state');
source.onmessage = function (event) {
  var msg = JSON.parse(event.data);
  //if (!globmsg) {
    console.log('FIRST', msg);
    //$('body').removeClass('disabled')
    //map.getView().setCenter(ol.proj.transform([msg.lon, msg.lat], 'EPSG:4326', 'EPSG:3857'));
  //}
  globmsg = msg;

  $('#header-state').html('<b>Armado:</b> ' + msg.armed + '<br><b>Modo:</b> ' + msg.mode + '<br><b>Altura:</b> ' + msg.alt.toFixed(2) + '<br><b>Latitud:</b> ' + msg.lat + '<br><b>Longitud:</b> ' + msg.lon)
  $('#e-d-armado').html(msg.armed);
  $('#e-d-modo').html(msg.mode);
  $('#e-d-altura').html(msg.alt.toFixed(2));
  //$('#muestra').html(msg.idm+'-'+msg.tipom+msg.distact+'-'+msg.distini+'-'+msg.idf+'-'+msg.xf+'-'+msg.yf+'-'+msg.hf+'-'+msg.ruta);
  conexion=msg.conectado
  //alert(conexion)
  $('#idm').html(msg.idm);
  $('#tipom').html(msg.tipom);
  $('#idf').html(msg.idf);
  $('#coordf').html(msg.xf+'<br>'+msg.yf+'<br>'+msg.hf);
  $('#distini').html(parseFloat(msg.distini).toFixed(5));
  $('#distact').html(parseFloat(msg.distact).toFixed(5));
  //$('#foto').html("<img src='"+msg.ruta+"' width='200'/>");
  //Obtener el chequeado antes de borrarlo
  idsel=$('#selrec').find("option:selected").val();

  $('#bateria').html(msg.bateria+"%");
  //$('#satelites').html(msg.satelites);

  if (entreCombo==false) {
    $('#selrec').html("<option value='0'>Ningún recorrido</option>");
      $.each( msg.recorridos, function( key, nuevorec ) {
        //alert( key + ": " + value );
        recorridos.splice(0,contcoord);
        contrec=0;
        recorridos[contrec]=nuevorec;
        var hsel=""
        if (idsel==nuevorec.idr){
            hsel="selected='selected'"
        }
        $('#selrec').append("<option value='"+nuevorec.idr+"' "+hsel+" >"+nuevorec.idr+"_("+nuevorec.padron+")</option>");
      });

  }


  arm=msg.armed;
  //$('#header-arm').prop('disabled', msg.armed);
};

//Funciones generales

jQuery.fn.swap = function(b){ 
    b = jQuery(b)[0]; 
    var a = this[0]; 
    var t = a.parentNode.insertBefore(document.createTextNode(''), a); 
    b.parentNode.insertBefore(a, b); 
    t.parentNode.insertBefore(b, t); 
    t.parentNode.removeChild(t); 
    return this; 
};
