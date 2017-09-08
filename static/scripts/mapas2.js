if (typeof L !== 'undefined') {
    console.log("No es indefinido");
    var map = L.map('map').setView([-32.3160, -58.08357954025450], 17);
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '',
								      maxZoom: 18}).addTo(map);
    L.control.scale().addTo(map);

    var green = 0;
    var orange = 0;
    var red = 0;
    var contador = 0;
    var markers = {};

    function onLocationFound(e) {
	var radius = e.accuracy / 2;
	var location = e.latlng;
	L.marker(location).addTo(map);
	L.circle(location, radius).addTo(map);
    }

    function onLocationError(e) {
	alert(e.message);
    }

    function getLocationLeaflet() {
	map.on('locationfound', onLocationFound);
	map.on('locationerror', onLocationError);

	map.locate({setView: true, maxZoom: 16});
    }
    getLocationLeaflet();


    var popup = L.popup();

    function onMapClick(e) {
	console.log(coordenadas);
	//console.log("Altura: " + altura);
	var marcador = L.marker(e.latlng);
	marcador.addTo(map);
	marcador.on('click', onMarkerClick);
	contador ++;
	markers[contador] = marcador;

	obtenerAltura(e.latlng, contador);
	
	marcador.bindTooltip("Nro: " + contador, {permanent: true, className: "my-label", offset: [0, 0] });
	agregarMarcadorTabla(marcador, contador);
    }

    function agregarMarcadorTabla(marcador, nombre){
	var tbody = document.getElementById("puntosrec").querySelectorAll("tbody")[0];
	var row = document.createElement("tr");

	var cell1 = document.createElement("td");
	var cell2 = document.createElement("td");
	var cell3 = document.createElement("td");
	var cell4 = document.createElement("td");
	var cell5 = document.createElement("td");

	var span = document.createElement("SPAN");
	var txt = document.createTextNode("\u00D7");
	span.className = "close";
	span.appendChild(txt);

	span.onclick = function(){
	    var element = document.getElementById("ID-"+nombre);
	    element.parentNode.removeChild(element);
	    map.removeLayer(markers[nombre]);
	    markers[nombre] = 0;
	}

	cell1.appendChild(span);

	var alt = marcador.getLatLng().alt;
	if(alt == "undefined") alt = "";
	cell2.appendChild(document.createTextNode(nombre));
	cell3.appendChild(document.createTextNode(marcador.getLatLng().lat));
	cell4.appendChild(document.createTextNode(marcador.getLatLng().lng));
	cell5.appendChild(document.createTextNode(alt));
	
	row.appendChild(cell1);
	row.appendChild(cell2);
	row.appendChild(cell3);
	row.appendChild(cell4);
	row.appendChild(cell5);

	row.id = "ID-"+nombre;
	tbody.appendChild(row);
	
    }

    function borrar(nodo){
	console.log("Borrar " + nodo);
    }

    function onMarkerClick(e) {
	
	popup
	    .setLatLng(e.latlng)
	    .setContent("Click aca" )
	    .openOn(map);
    }

    map.on('click', onMapClick);


    function agregarPunto(){
	var nombre = document.getElementById("nombrePunto").value;
	var latitud = document.getElementById("y").value;
	var longitud = document.getElementById("x").value;
	var altura = parseFloat(document.getElementById("h").value);
	console.log("Nombre: " + nombre + " Latitud: " + latitud + " longitud: " + longitud);
	var latlng = L.latLng(latitud, longitud, altura);

	
	var marcador = L.marker(latlng);
	marcador.addTo(map);
	marcador.on('click', onMarkerClick);
	
	markers[nombre] = marcador;

	marcador.bindTooltip(nombre, {permanent: true, className: "my-label", offset: [0, 0] });
	agregarMarcadorTabla(marcador, nombre);

    }

    function inicioGoogle(){
	console.log("Inicio");
    }

    function obtenerAltura(latlng, nombre){
	var elevator = new google.maps.ElevationService;

	elevator.getElevationForLocations({
	    'locations': [latlng]
	}, function(results, status) {
	    console.log("Estado: " + status);
	    if (status === 'OK') {
		// Retrieve the first result
		if (results[0]) {
		    console.log("Elevacion: " + results[0].elevation);
		    jQuery(jQuery("#ID-" + nombre).children()[4]).text(results[0].elevation);
		} else {
		    console.log('No results found');
		}
	    } else {
		console.log('Elevation service failed due to: ' + status);
	    }
	});
    } 
} else  console.log("Es indefinido");
			
