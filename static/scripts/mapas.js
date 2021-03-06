if (typeof L !== 'undefined') {
    console.log("No es indefinido");
    var map = L.map('map').setView([-32.3160, -58.08357954025450], 17);
    //L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {attribution: '',
	//							      maxZoom: 30}).addTo(map);
    
	/*var HERE_hybridDay = L.tileLayer('http://{s}.{base}.maps.cit.api.here.com/maptile/2.1/{type}/{mapID}/hybrid.day/{z}/{x}/{y}/{size}/{format}?app_id={app_id}&app_code={app_code}&lg={language}', {
		attribution: 'Map &copy; 1987-2014 <a href="http://developer.here.com">HERE</a>',
		subdomains: '1234',
		mapID: 'newest',
		app_id: 'K6SEXfDdlUMQKAJx2FQJ',
		app_code: 'Y2K8gHDWWBqr4J-FYjNXCA',
		base: 'aerial',
		maxZoom: 20,
		type: 'maptile',
		language: 'eng',
		format: 'png8',
		size: '256'
	}).addTo(map);*/

	googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
		maxZoom: 20,
		subdomains: ['mt0', 'mt1', 'mt2', 'mt3']	
	}).addTo(map);

    L.control.scale().addTo(map);

    var green = 0;
    var orange = 0;
    var red = 0;
    var contador = 0;
    var markers = {};
    var rectangulo;
	var polygon;
	var popupEditar;
	var esquinasMandar = [];
	var puntoInicial;

    function onLocationFound(e) {
		var radius = e.accuracy / 2;
		var location = e.latlng;
		L.marker(location).addTo(map);
		L.circle(location, radius).addTo(map);
    }

    function onLocationError(e) {
		console.log(e.message);
    }

    function getLocationLeaflet() {
		map.on('locationfound', onLocationFound);
		map.on('locationerror', onLocationError);

	//	map.locate({setView: true, maxZoom: 16});
    }
    getLocationLeaflet();

    function getAlturaEstandar(){
    	if(isNaN(parseFloat(document.getElementById("alt").value))) 
		return 20;
	else 
		return parseFloat(document.getElementById("alt").value);
    }

    var popup = L.popup();

    function onMapClick(e) {
	    var nombreDeEsteMark = "";
	    
	    var alturaActual = getAlturaEstandar();
	  	e.latlng.alt = alturaActual;
	    console.log("PI");
	    console.log(puntoInicial);
	    console.log("PI2");
	    if(!puntoInicial){
    		var redMarker = L.ExtraMarkers.icon({
			    icon: 'fa-flag',
			    markerColor: 'green',
			    shape: 'circle',
			    prefix: 'fa'
	  		});
    		console.log(e.latlng);
		  	marcador = L.marker(e.latlng, {icon: redMarker, draggable: true}).addTo(map);
		  	marcador.on('click', onMarkerClick);
		  	nombreDeEsteMark = "Punto Inicial";
		  	puntoInicial = marcador;
	    }else {
	    	var marcador = L.marker(e.latlng,{
			    draggable: true
			});
		    marcador.addTo(map);
		    marcador.on('click', onMarkerClick);
		    contador ++;

		    while(!noExisteNombreDeCoordenada(contador)){
		    	//si ya existe este, aumentamos el contador
		    	contador++;
		    }
		    nombreDeEsteMark = ""+contador;
	    }
	    markers[nombreDeEsteMark] = marcador;
	    var nuevac = {
		    nombre: nombreDeEsteMark,
		    x: e.latlng.lat,
		    y: e.latlng.lng,
		    h: alturaActual,
		    tipo: 1
		};
		obtenerAltura(e.latlng, nombreDeEsteMark, coordenadas, contcoord, nuevac);
		contcoord ++;
		
		marcador.on("dragend", terminaMovimientoMarcador);

	    marcador.bindTooltip(nombreDeEsteMark, {permanent: true, className: "my-label", offset: [0, 0] });
	    agregarMarcadorTabla(marcador, nombreDeEsteMark);

	    verSiHayQueDibujarRectangulo();

	}

    /*Funcion cuando termina el movimiento del marcador, hay que actualizar la tabla y la variable coordenadas*/
    function terminaMovimientoMarcador(e){
		var nombreActual = obtenerNombreMarcador(this);
		console.log("hola");
		//console.log("");
		if(nombreActual){
		   	//actualizarlo en la tabla
			jQuery(jQuery("#ID-" + nombreActual.replace(" ", "_")).children()[2]).text(this.getLatLng().lat);
		   	jQuery(jQuery("#ID-" + nombreActual.replace(" ", "_")).children()[3]).text(this.getLatLng().lng);
		   		
		   	var res = obtenerCoordenadaDesdeNombre(nombreActual);
		   	if(res){
		   		var coordenadaActual = res[0];
		   		var indiceActual = res[1];
		   		var otraCoor = {
				    nombre: nombreActual,
				    x: this.getLatLng().lat,
				    y: this.getLatLng().lng,
				    h: 0,
				    tipo: coordenadaActual['tipo']
				};
		   		obtenerAltura(this.getLatLng(), nombreActual, coordenadas, indiceActual, otraCoor);
		   	}
		}
		if((Object.keys(markers).length == 4 || (Object.keys(markers).length == 5 && puntoInicial)) && rectangulo){
			dibujarRectangulo();
		}
	}

	function verSiHayQueDibujarRectangulo(){
		if((Object.keys(markers).length == 5 || (Object.keys(markers).length == 4) && puntoInicial)){
			dibujarRectangulo();
		}
	}

	/* Obtiene el nombre del marcador recibiendo el marcador (el objeto en si no puede guardar el nombre) */
	function obtenerNombreMarcador(marcador){
		var idLeaflet = marcador['_leaflet_id'];
		for (var i in markers){
			console.log(markers[i]);
			console.log(i);
			if(idLeaflet == markers[i]['_leaflet_id'])
				return i;
		}
		return null;
	}

	/* Obtiene una coordenada del array a partir del nombre */
	function obtenerCoordenadaDesdeNombre(nombre){
		for (var i in coordenadas){
			if(coordenadas[i]['nombre'] == nombre){
				return [coordenadas[i], i];
			}
		}
		return null;
	}

	/* Agrega los datos del marcador a la tabla */
    function agregarMarcadorTabla(marcador, nombre){
		var tbody = document.getElementById("puntosrec").querySelectorAll("tbody")[0];
		var row = document.createElement("tr");

		var cell1 = document.createElement("td");
		var cell2 = document.createElement("td");
		var cell3 = document.createElement("td");
		var cell4 = document.createElement("td");
		var cell5 = document.createElement("td");
		var cell6 = document.createElement("td");

		var span = document.createElement("SPAN");
		var txt = document.createTextNode("\u00D7");
		span.className = "close";
		span.appendChild(txt);

		span.onclick = function(){
	  		var idDelTR = jQuery(this).closest("tr").attr('id');
  			var partes = idDelTR.split("ID-");
  			var nombreDeAhora = partes[1].replace("_", " ");
	  		var element = document.getElementById(idDelTR);
			element.parentNode.removeChild(element);
			if(markers[nombreDeAhora] == puntoInicial)
				puntoInicial = null;
			map.removeLayer(markers[nombreDeAhora]);
			delete markers[nombreDeAhora];
	  	}

		cell1.appendChild(span);

		var alt = marcador.getLatLng().alt;
		if(alt == "undefined") alt = "";
		cell2.appendChild(document.createTextNode(nombre));
		cell3.appendChild(document.createTextNode(marcador.getLatLng().lat));
		cell4.appendChild(document.createTextNode(marcador.getLatLng().lng));
		cell5.appendChild(document.createTextNode(alt));
		if(marcador == puntoInicial)
			cell6.appendChild(document.createTextNode('Estaca'));
		else
			cell6.appendChild(document.createTextNode('Común'));
		row.appendChild(cell1);
		row.appendChild(cell2);
		row.appendChild(cell3);
		row.appendChild(cell4);
		row.appendChild(cell5);
		row.appendChild(cell6);

		row.id = "ID-"+nombre.replace(" ", "_");
		tbody.appendChild(row);
	
    }

    /* Funcion cuando se hace click en un marcador, se abre una ventana para editarlo */
    function onMarkerClick(e) {
		//abrimos una ventana para editar
	    var nombre = obtenerNombreMarcador(e.target);
	    var latLng = e.target.getLatLng();
	    var lat = latLng.lat;
	    var lng = latLng.lng;
	    var altura = jQuery(jQuery("#ID-" + nombre.replace(" ", "_")).children()[4]).text();


	    popupEditar = popup
	        .setLatLng(e.latlng)
	        .setContent('<input type="hidden" id="popupNombreOrig" value="'+nombre+'"/><h4 style="text-align:center;">Editar</h4><table style="border-spacing: 5px;border-collapse: separate;margin-top:5px;"><tr><td>Nombre:</td> <td><input type="text" id="popupNombre" value="'+nombre+'"/></td> </tr> <tr><td>Latitud:</td> <td><input type="text" id="popupLat" value="'+lat+'"/> </td></tr> <tr><td>Longitud:</td> <td><input type="text" id="popupLng" value="'+lng+'"/></td> </tr> <tr><td>Altura:</td> <td><input type="text" id="popupAlt" value="'+altura+'"/></td> </tr></table> <table style="style="border-spacing: 5px;border-collapse: separate;width:100%;margin-top: 5px;"><tr><td style="width:33%;"><button class="button-success pure-button" onclick="editarMarcador();" style="color: white;border-radius: 4px;text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);background: rgb(28, 184, 65);">Guardar</button></td><td style="width:33%;"><button onclick="definirPuntoInicial();" class="button-secondary pure-button" style="color: white;border-radius: 4px;text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);background: rgb(66, 184, 221);">Definir PI</button></td><td style="width:33%;"><button onclick="borrarMarcador();"  class="button-warning pure-button" style="background: rgb(202, 60, 60);color: white;border-radius: 4px;text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);">Borrar</button></td></tr></table><style>.table {border-spacing: 5px;}</style>' )
	        .openOn(map);  
	}

	function borrarMarcador(){
		var nombreMarcador = jQuery("#popupNombreOrig").val();
		var marcadorActual = markers[nombreMarcador];

		var auxLL = marcadorActual.getLatLng();
		
		console.log("BORRA ESTE --------");
		console.log(nombreMarcador);
		console.log(marcadorActual);
		console.log("PuntoI");
		console.log(puntoInicial);
		if(puntoInicial == marcadorActual){
			puntoInicial = null;
			console.log("Es el punto inicial");
		}
		else
			console.log("no es el punto inu");

		var elId = "ID-" + nombreMarcador.replace(" ", "_");
  		var element = document.getElementById(elId);
		element.parentNode.removeChild(element);
		map.removeLayer(markers[nombreMarcador]);
		delete markers[nombreMarcador];


		//console.log(element);

		console.log("BORRA ESTE --------");
	    //cerramos el popup
	    map.closePopup();
	}

	function definirPuntoInicial(){
		var nombreMarcador = jQuery("#popupNombreOrig").val();
		var marcadorActual = markers[nombreMarcador];

		var auxLL = marcadorActual.getLatLng();
		
		//convierte el marcador punto inicial en un marker normal
		convertirPuntoInicialToNormal();
		//borrar el actual
		map.removeLayer(markers[nombreMarcador]);
		delete markers[nombreMarcador];

		//creamos el nuevo
		var greenMarker = L.ExtraMarkers.icon({
		    icon: 'fa-flag',
		    markerColor: 'green',
		    shape: 'circle',
		    prefix: 'fa'
  		});

		marcadorNuevo = L.marker(auxLL, {icon: greenMarker, draggable: true}).addTo(map);
	  	marcadorNuevo.on('click', onMarkerClick);
	    markers[nombreMarcador] = marcadorNuevo;			
		marcadorNuevo.on("dragend", terminaMovimientoMarcador);
	    marcadorNuevo.bindTooltip(nombreMarcador, {permanent: true, className: "my-label", offset: [0, 0] });

	    puntoInicial = marcadorNuevo;

	    if(rectangulo){
	    	// lo dibujamos de vuelta
	    	dibujarRectangulo();
	    }

	    //cerramos el popup
	    map.closePopup();
	}

	function convertirPuntoInicialToNormal(){
		// si hay punto inicial tenemos que convertirlo en uno normal
		if(puntoInicial){
			console.log(puntoInicial);
			var nombrePI = obtenerNombreMarcador(puntoInicial);
			var auxLL = puntoInicial.getLatLng();
			//borrar el inicial
			map.removeLayer(markers[nombrePI]);
			delete markers[nombrePI];

			//creamos el nuevo
			marcadorNuevo = L.marker(auxLL,{draggable: true}).addTo(map);
		  	marcadorNuevo.on('click', onMarkerClick);
		    markers[nombrePI] = marcadorNuevo;			
			marcadorNuevo.on("dragend", terminaMovimientoMarcador);
		    marcadorNuevo.bindTooltip(nombrePI, {permanent: true, className: "my-label", offset: [0, 0] });
		}
	}

	/* Funcion para cambiar el nombre de la coordenada de nombre1 al nombre2 */
	function cambiarNombreCoordenada(nombre1, nombre2){
		var coor = obtenerCoordenadaDesdeNombre(nombre1);
		if(coor)
			coor[0]["nombre"] = nombre2;
	}

	/* Funcion para editar el marcador */
	function editarMarcador (){
		var nombreOriginal = jQuery("#popupNombreOrig").val();
		var nombre = jQuery("#popupNombre").val();
		var latitud = jQuery("#popupLat").val();
		var longitud = jQuery("#popupLng").val();
		var altura = jQuery("#popupAlt").val();
		var markActual = markers[nombreOriginal];

		if(markActual /*&& nombreOriginal == nombre*/){
			if(latitud && longitud && altura){
				//ajustar los elementos en la tabla
				if(nombre != nombreOriginal){
					document.getElementById("ID-" + nombreOriginal.replace(" ", "_")).id = "ID-" + nombre.replace(" ", "_");
					jQuery(jQuery("#ID-" + nombre.replace(" ", "_")).children()[1]).text(nombre);
			    	cambiarNombreCoordenada(nombreOriginal, nombre);
				}


				jQuery(jQuery("#ID-" + nombre).children()[1]).text(nombre);
				jQuery(jQuery("#ID-" + nombre).children()[2]).text(latitud);
				jQuery(jQuery("#ID-" + nombre).children()[3]).text(longitud);
				jQuery(jQuery("#ID-" + nombre).children()[4]).text(altura);
				//termina la parte de la tabla

				//borro el marcador viejo y creo uno nuevo
				map.removeLayer(markActual);
				map.removeLayer(popupEditar);
				var marcadorNuevo = L.marker([latitud, longitud, altura],{
				    draggable: true
				});

			    marcadorNuevo.addTo(map);
			    marcadorNuevo.on('click', onMarkerClick);
			    markers[nombre] = marcadorNuevo;

				marcadorNuevo.on("dragend", terminaMovimientoMarcador);

			    marcadorNuevo.bindTooltip(nombre, {permanent: true, className: "my-label", offset: [0, 0] });
			} else {
				new Noty({
				    type: 'error',
				    layout: 'topRight',
				    theme: 'mint',
	  			    text: 'Faltan datos para guardar',
				    timeout: 5000,
				    progressBar: true,
				    closeWith: ['click', 'button'],
				    animation: {
					open: 'noty_effects_open',
					close: 'noty_effects_close'
				    },
  				}).show()
			}
		}

		console.log("Nombre Original: " + nombreOriginal + " Nombre: " + nombre + " Latitud: " + latitud + " Longitud: " + longitud + " Altura: " + altura);
	}

    map.on('click', onMapClick);


    function agregarPunto(){
		//var nombre = document.getElementById("nombrePunto").value;
		var latitud = document.getElementById("y").value;
		var longitud = document.getElementById("x").value;
		var altura = parseFloat(document.getElementById("h").value);
		var latlng = L.latLng(longitud, latitud, altura);
		var nombre = ""+(contcoord + 1);
		if(noExisteNombreDeCoordenada(nombre)){
			$("#x").val("");
			$("#y").val("");
			$("#h").val("");
			$("#xrel").val("");
			$("#yrel").val("");
			$("#nombrePunto").val("");

			if(!puntoInicial){
	    		var redMarker = L.ExtraMarkers.icon({
				    icon: 'fa-flag',
				    markerColor: 'green',
				    shape: 'circle',
				    prefix: 'fa'
		  		});

			  	marcador = L.marker(latlng, {icon: redMarker, draggable: true}).addTo(map);
			  	marcador.on('click', onMarkerClick);
			  	puntoInicial = marcador;
		    }else {
		    	var marcador = L.marker(latlng,{
				    draggable: true
				});
			   
		    }

			marcador.addTo(map);
			marcador.on('click', onMarkerClick);
			
			markers[nombre] = marcador;

			marcador.on("dragend", terminaMovimientoMarcador);

			marcador.bindTooltip(nombre, {permanent: true, className: "my-label", offset: [0, 0] });
			agregarMarcadorTabla(marcador, nombre);

			verSiHayQueDibujarRectangulo();
			return true;
		}/* else {
			/*new Noty({
			    type: 'error',
			    layout: 'topRight',
			    theme: 'mint',
  			    text: 'Ya existe este nombre, elija otro',
			    timeout: 5000,
			    progressBar: true,
			    closeWith: ['click', 'button'],
			    animation: {
				open: 'noty_effects_open',
				close: 'noty_effects_close'
			    },
			}).show();
			return false;
		}*/

    }

    function inicioGoogle(){
		console.log("Inicio");
    }

    function noExisteNombreDeCoordenada(nombre){
		if(markers[nombre])
			return false;
		else
			return true;
		
	}

    function obtenerAltura(latlng, nombre, coor, cont, nueva){
    	coor[cont] = nueva;
		/*var elevator = new google.maps.ElevationService;

		elevator.getElevationForLocations({
		    'locations': [latlng]
		}, function(results, status) {
		    console.log("Estado: " + status);
		    if (status === 'OK') {
				if (results[0]) {
				    console.log("Elevacion: " + results[0].elevation);
				    jQuery(jQuery("#ID-" + nombre.replace(" ", "_")).children()[4]).text(results[0].elevation);
				    //agrego la nueva coordenada
				    nueva["h"] = results[0].elevation;
				    coor[cont] = nueva;
				   
				} else {
				    console.log('No results found');
				    coor[cont] = nueva;
				}
		    } else {
			console.log('Elevation service failed due to: ' + status);
			coor[cont] = nueva;
		    }
		});*/
    }

    function dibujarRectangulo(){
		if(rectangulo){
		    map.removeLayer(rectangulo);	
		    rectangulo = null;
		}

		if(polygon){
		    map.removeLayer(polygon);	
		    polygon = null;
		}
		
		if(Object.keys(markers).length == 4 || (Object.keys(markers).length == 5 && puntoInicial)){	
		    for (var i in markers){
			if(markers[i] != puntoInicial){
				    var minLong = parseFloat(markers[i].getLatLng().lng);
				    var minLat = parseFloat(markers[i].getLatLng().lat);
				    var maxLong = parseFloat(markers[i].getLatLng().lng);
				    var maxLat = parseFloat(markers[i].getLatLng().lat);

				    puntoMaxLat = [markers[i].getLatLng().lat, markers[i].getLatLng().lng];
				    puntoMinLat = [markers[i].getLatLng().lat, markers[i].getLatLng().lng];

			    break;
			    }
			}
		        
		        polygonPoints = [];

		        puntoMaxLat = [];
		        puntoMinLat = [];

		        //guardo el punto de mayor latitud y el de menor latitud..
		    for (var i in markers){
				if(markers[i] != puntoInicial){
			    	polygonPoints.push([markers[i].getLatLng().lat, markers[i].getLatLng().lng]);
			    	if(markers[i].getLatLng().lat > maxLat){
			    		maxLat = parseFloat(markers[i].getLatLng().lat);
			    		puntoMaxLat = [markers[i].getLatLng().lat, markers[i].getLatLng().lng];
			    	}
			    	if(markers[i].getLatLng().lng > maxLong)
			    		maxLong = parseFloat(markers[i].getLatLng().lng);
			    	if(markers[i].getLatLng().lng < minLong)
			    		minLong = parseFloat(markers[i].getLatLng().lng);
			    	if(markers[i].getLatLng().lat < minLat){
			    		minLat = parseFloat(markers[i].getLatLng().lat);
			    		puntoMinLat = [markers[i].getLatLng().lat, markers[i].getLatLng().lng];
			    	}
				}
		    }

			// 2 vertices opuestos del rectangulo tiene que ser..
	   		esquinas = [[maxLat, maxLong], [minLat, minLong]];

	   		var redMarker = L.ExtraMarkers.icon({
			    icon: 'fa-flag',
			    markerColor: 'green',
			    shape: 'circle',
			    prefix: 'fa'
	  		});

	   		// polygon = new L.Polygon(polygonPoints, {color: "red", weight: 1});
        // map.addLayer(polygon); 
	   		/*
	   		marcador1 = L.marker([minLat, minLong], {icon: redMarker, draggable: true}).addTo(map);
	   		marcador2 = L.marker([minLat, maxLong], {icon: redMarker, draggable: true}).addTo(map);
	   		marcador3 = L.marker([maxLat, maxLong], {icon: redMarker, draggable: true}).addTo(map);
	   		*/
	   		var punto1 = {
			    x: minLat,
			    y: minLong,
			    h: getAlturaEstandar(),
			    tipo: 1
			};
			var punto2 = {
			    x: minLat,
			    y: maxLong,
			    h: getAlturaEstandar(),
			    tipo: 1
			};
			var punto3 = {
			    x: maxLat,
			    y: maxLong,
			    h: getAlturaEstandar(),
			    tipo: 1
			};
	   		esquinasMandar = [punto1,punto2,punto3];

		    rectangulo = L.rectangle(esquinas, {color: "blue", weight: 1}).addTo(map);
	   	} else 			
	   		new Noty({
			    type: 'error',
			    layout: 'topRight',
			    theme: 'mint',
	  		    text: 'Debe tener exactamente cuatro puntos para calcular el &aacute;rea',
			    timeout: 5000,
			    progressBar: true,
			    closeWith: ['click', 'button'],
			    animation: {
				open: 'noty_effects_open',
				close: 'noty_effects_close'
			    },
  			}).show()
   		
	} 

	function limpiarMapa(){
		for (var i in markers){
			map.removeLayer(markers[i]);
			delete markers[i];
	    }

	    if(puntoInicial) puntoInicial = null;

		//borrar de la tabla
		var n = 0;
		$('#puntosrec tr').each(function() {
		   if (n > 0)
		      $(this).remove();
		   n++;
		});
		contador = 0;

		borrarRectangulo();
    }
    function borrarRectangulo(){
	    if(rectangulo){
		    map.removeLayer(rectangulo);	
		    rectangulo = null;
		}

		if(polygon){
		    map.removeLayer(polygon);	
		    polygon = null;
		}
    }

    function cargarGpx(){
	var fechaMin = document.getElementById("fechaGpx1").value;
	var fechaMax = document.getElementById("fechaGpx2").value;
	$.ajax({
	    method: 'POST',
	    url: '/api/cargargpx',
	    contentType : 'application/json',
	    data: JSON.stringify({fechaMin: fechaMin, fechaMax: fechaMax})
	    })
	    .done(function( msg ) {
	        var data = msg;
	        if(data == "No hay archivo"){
			    new Noty({
				    type: 'warning',
				    layout: 'topRight',
				    theme: 'mint',
		  		    text: 'No hay ning&uacute;n archivo .gpx en las Unidades extra&iacute;bles',
				    timeout: 5000,
				    progressBar: true,
				    closeWith: ['click', 'button'],
				    animation: {
					open: 'noty_effects_open',
					close: 'noty_effects_close'
				    },
	  		    }).show();
			    return;
	        }
	        if(data == "0"){
			    new Noty({
				    type: 'warning',
				    layout: 'topRight',
				    theme: 'mint',
		  		    text: 'El archivo no tiene puntos para cargar o ninguno coincide con los criterios de b&uacute;squeda',
				    timeout: 5000,
				    progressBar: true,
				    closeWith: ['click', 'button'],
				    animation: {
					open: 'noty_effects_open',
					close: 'noty_effects_close'
				    },
	  		    }).show();
			    return;
	        }
	        if(data == 'No hay pendrive'){
	      		new Noty({
				    type: 'warning',
				    layout: 'topRight',
				    theme: 'mint',
		  		    text: 'No hay pendrive conectado',
				    timeout: 5000,
				    progressBar: true,
				    closeWith: ['click', 'button'],
				    animation: {
					open: 'noty_effects_open',
					close: 'noty_effects_close'
				    },
	  		    }).show();
			    return;
	        }

	        if(data == 'No hay carpeta'){
	      		new Noty({
				    type: 'warning',
				    layout: 'topRight',
				    theme: 'mint',
		  		    text: 'No existe la carpeta "coordenadasDron" en el pendrive',
				    timeout: 5000,
				    progressBar: true,
				    closeWith: ['click', 'button'],
				    animation: {
					open: 'noty_effects_open',
					close: 'noty_effects_close'
				    },
	  		    }).show();
			    return;
	        }

	        console.log(data);

	    	datanueva = data.split("{");
	    	//console.log(Object.keys(data).length);
	    	for (var i in datanueva){
	    		var nom = "";
	    		var lat = "";
	    		var lng = "";
	    		var alt = "";
	    		if(datanueva[i] != "[" && datanueva[i] != "{" && datanueva[i]){
	    			//console.log("Linea: " + datanueva[i]);
		    		var lineas = datanueva[i].split("}")[0];
		    		//console.log(lineas);
		    		var datos = lineas.split(",");
		    		//console.log(datos);
		    		//console.log("Nombre");
		    		if(datos[0].indexOf("nombre") != -1){
		    			nom = datos[0].split("'")[1];
		    		}
		    		if(datos[1].indexOf("latitud") != -1){
		    			lat = datos[1].split("'")[1];
		    		}
		    		if(datos[2].indexOf("longitud") != -1){
		    			lng = datos[2].split("'")[1];
		    		}
		    		/*if(datos[3].indexOf("altitude") != -1){
		    			alt = datos[3].split("'")[1];
		    		}*/
		    		//console.log("Data: |"+nom+"|"+lat+"|"+lng);
		    		/*---------------------------------------------------*/
		    		if(nom && lat && lng){
	    				var latlng = L.latLng(lat, lng, alt);
			    		var marcador = L.marker(latlng,{
						    draggable: true
						});
					map.setView(latlng, 17);

					marcador.addTo(map);
					    marcador.on('click', onMarkerClick);

					    markers[nom] = marcador;

					    var nuevac = {
						    nombre: nom,
						    x: lat,
						    y: lng,
						    h: alt,
						    tipo: 1
						};

						coordenadas[contcoord] = nuevac;
						contcoord ++;
								
						marcador.on("dragend", terminaMovimientoMarcador);
				
					    marcador.bindTooltip( nom, {permanent: true, className: "my-label", offset: [0, 0] });
					    agregarMarcadorTabla(marcador, nom);
			    		}
						    /*---------------------------------------------------*/
		    		}
			    	
		}
	      new Noty({
			type: 'success',
			layout: 'topRight',
			theme: 'mint',
	  		text: 'Datos cargados exitosamente',
			timeout: 5000,
			progressBar: true,
			closeWith: ['click', 'button'],
			animation: {
				open: 'noty_effects_open',
				close: 'noty_effects_close'
			},
  		}).show()
	  });
    }

    function ordenarCoordenadas(){
    	console.log("Coordenadas:");
    	console.log(coordenadas);
    		
    	var nuevasCoordenadas = [];
    	if(puntoInicial){
    		console.log("Hay punto Inicial");
    		coorPI = puntoInicial.getLatLng();
    		var nuevaCoor = [coorPI.lng, coorPI.lat];
    		var nuevaCoor = {
			    x: coorPI.lat,
			    y: coorPI.lng,
			    h: getAlturaEstandar(),
			    tipo: 0
			};
    		nuevasCoordenadas.push(nuevaCoor);
    	} else{
    		new Noty({
				type: 'error',
				layout: 'topRight',
				theme: 'mint',
		  		text: 'No se puede guardar el recorrido sin un Punto Inicial definido',
				timeout: 5000,
				progressBar: true,
				closeWith: ['click', 'button'],
				animation: {
					open: 'noty_effects_open',
					close: 'noty_effects_close'
				},
	  		}).show();
	  		return false;
    	} 

    	for (var i in esquinasMandar){
    		nuevasCoordenadas.push(esquinasMandar[i]);
    	}
    	console.log("Vertices:");
    	console.log(esquinasMandar);

    	console.log("Nuevas:");
    	console.log(nuevasCoordenadas);
    	coordenadas = nuevasCoordenadas;
    	return true;

    }
    
} else  console.log("Es indefinido");
			
