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
//alert("mi dato" + dato);
  return isNaN(parseInt(dato))
}

$('#header-arm').on('click', function () {
  var armenv=1;
  //si esta armado hay que desarmar
  if (arm==true) armenv=0;
  if (!conexion){
	alert("No está conectado");
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
	alert("No está conectado");
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
	alert("Para ingresar una coordenada debe ingresar 2 valores numericos válidos para la altura y la valocidad");
	}
  else
	{
	  $.ajax({
	    method: 'PUT',
	    url: '/api/iniciarmision',
	    contentType : 'application/json',
	    data: JSON.stringify({ umbral:umbral, resolucion:resolucion, demora:demora, movfotos:movfotos, altitud:altitud}),
	  })
	  .done(function( msg ) {
	    console.log('Mision finalizada')
	    if (msg.ok==false) alert("No fue posible completar la misión. Verifique haber ingresado coordenadas")
	  });
	}
})

$('#header-despegar').on('click', function () {
  if (!conexion){
	alert("No está conectado");
	return;
  }

  var v=$("#vel").val();
  var h=$("#alt").val();
  if (mal(v) || mal(h)){
	alert("Para ingresar una coordenada debe ingresar 2 valores numericos válidos para la altura y la valocidad");
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
	    console.log('Mision finalizada')
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
	alert("Para ingresar una coordenada debe ingresar 2 valores numericos válidos para la altura y la valocidad");
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
    alert(msg.ok)
    console.log('FOTO SACADA')
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
    $("#puntosrec").html("<tr><td>id</td><td>x</td><td>y</td><td>h</td><td>tipo</td></tr>");
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
			$("#padron").val(msg.recorrido.padron)
			$("#alt").val(msg.recorrido.alt)
			$("#vel").val(msg.recorrido.vel)
			$("#cantpuntos").val(msg.recorrido.cantpuntos)
			$("#calculodist").val(msg.recorrido.calculodist)
			if (msg.recorrido.umbral==0){
			    $("#umbral").val(0.5)
			    }
			else{
			    $("#umbral").val(msg.recorrido.umbral*2)
			}

			$("#tipo").val(mostrarTipoRec(msg.recorrido.tipo))
			$("#puntosrec").html("<tr><td>id</td><td>x</td><td>y</td><td>h</td><td>tipo</td></tr>");
			$.each( msg.puntos, function( key, punto ) {
			  	//alert( key + ": " + value );
			  	$("#puntosrec").append("<tr><td>"+punto.id+"</td><td>"+punto.x+"</td><td>"+punto.y+"</td><td>"+punto.h+"</td><td>"+mostrarTipoAI(punto.tipo)+"</td></tr>");
			  });

			console.log('RECORRIDO LEIDO')
		}else{
			alert("No fue posible seleccionar el recorrido");
		}
	});
	}
})


$('#guardar-recorrido').on('click', function () {
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
	alert("Para dar de alta el recorrido debe ingresar 3 valores numericos válidos para el padrón, la altura y la velocidad");
	}
  else
	{
	if (contcoord<=0){
		alert("Debe ingresar al menos un punto para poder dar de alta un recorrido nuevo");
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

				alert("RECORRIDO GUARDADO");
				console.log('RECORRIDO GUARDADO')
			}else{	
				alert("No fue posible dar de alta el recorrido");
			}
		});
		}
	}
})

$('#header-del-mision').on('click', function () {
  //coordenadas[contcoord]=[];
  coordenadas.splice(0,contcoord);
  contcoord=0;
  $("#puntosrec").html("<tr><td>x</td><td>y</td><td>h</td><td>tipo</td></tr>");
})

$('#header-add-coordenada').on('click', function () {
  var x=$("#x").val();
  var y=$("#y").val();
  var h=$("#h").val();
  var tipop=$("#tipop").val();
  var rel=$("#relativas").is(":checked");
  var xr=$("#xrel").val();
  var yr=$("#yrel").val();
  if (mal(x) || mal(y) || mal(h)){
	alert("Para ingresar una coordenada debe ingresar 3 valores numericos válidos para la altura, x e y");
	}
  else
	{
	//Si estamos poniendo coordenadas absolutas hay que revisar que hayan puesto la primera relativa
	if (!rel && (contcoord<1)){
	    if (mal(xr) || mal(yr)){
	        alert("Debe ingresar 2 valores numericos válidos para las coordenadas relativas solicitadas");
	        return false;
	    }else{
	        xrel=xr;
	        yrel=yr;
	        //ocultamos las opciones de absolutas porque solo la primera se ingresa la relativa
	        $("#opcionesabsolutas").hide();
	    }
	}
	//Agregamos las coordenadas de mantera local
	var nuevac = {
	    x: x,
	    y: y,
	    h: h,
	    tipo:tipop
	}
	coordenadas[contcoord]=nuevac;
	$("#x").val("");
	$("#y").val("");
	$("#h").val("");
    $("#xrel").val("");
    $("#yrel").val("");

	$("#puntosrec").append("<tr><td>"+x+"</td><td>"+y+"</td><td>"+h+"</td><td>"+mostrarTipoAI(tipop)+"</td></tr>");

	//alert("Coordenada agregada "+JSON.stringify(coordenadas));
	console.log('Coordenada agregada');
	contcoord++;
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



$('#header-conectar').on('click', function () {

var sim=$("#simular").is(":checked");
//alert(sim);
  $.ajax({
    method: 'PUT',
    url: '/api/conectar',
    contentType : 'application/json',
    //data: JSON.stringify({ cadena: 'tcp:192.168.42.12:5760' }),
    //data: JSON.stringify({ cadena: 'udp:127.0.0.1:14550' })
    data: JSON.stringify({ cadena: $("#cadena").val(), sim:sim })
  })
  .done(function( msg ) {
    if (msg.ok) {
		alert("Conectado!");		
		conexion=true
		$("#selrec").val(0).change();
		}
    else alert("No fue posicle conectarse");
    console.log('se conectó? ' + msg.ok)
  });
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



$('#header-desconectar').on('click', function () {
  $.ajax({
    method: 'PUT',
    url: '/api/desconectar',
    contentType : 'application/json'
  })
  .done(function( msg ) {
    if (msg.ok) {
		alert("Desconectado");		
		conexion=false
		$("#selrec").val(0).change();
		}
    else alert("No fue posicle desconectarse");
    console.log('se desconectó? ' + msg.ok)
  });
})


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

  //$('#muestra').html(msg.idm+'-'+msg.tipom+msg.distact+'-'+msg.distini+'-'+msg.idf+'-'+msg.xf+'-'+msg.yf+'-'+msg.hf+'-'+msg.ruta);
  conexion=msg.conectado
  //alert(conexion)
  $('#idm').html(msg.idm);
  $('#tipom').html(msg.tipom);
  $('#idf').html(msg.idf);
  $('#coordf').html(msg.xf+'-'+msg.yf+'-'+msg.hf);
  $('#distini').html(msg.distini);
  $('#distact').html(msg.distact);
  //$('#foto').html("<img src='"+msg.ruta+"' width='200'/>");
  //Obtener el chequeado antes de borrarlo
  idsel=$('#selrec').find("option:selected").val();

  $('#bateria').html(msg.bateria+"%");
  $('#satelites').html(msg.satelites);

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