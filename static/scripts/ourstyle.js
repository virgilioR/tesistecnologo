(function (window, document) {
    $(document).ready(function() {
        adecuar_modal();
        ocultar_hiddenconboton();
	var source = new EventSource('/api/sse/state');
	source.onmessage = function (event) {
	    var msg = JSON.parse(event.data);  
	    conexion=msg.conectado
	    if(conexion){
		console.log("ALGOOO");
		$('#header-conectar-desconectar').removeClass('button-success');
		$('#header-conectar-desconectar').removeClass('pure-button-disabled');
		$('#header-conectar-desconectar').addClass('button-error');
		$('#conect-desc-span').text('Desconectar');
		$('#iconocargando').hide();
		$('#conect-desc-span').show();
	    } else {
		$('#header-conectar-desconectar').removeClass('button-error');
		$('#header-conectar-desconectar').removeClass('pure-button-disabled');
		$('#header-conectar-desconectar').addClass('button-success');
		$('#conect-desc-span').text('Conectar');
		$('#iconocargando').hide();
		$('#conect-desc-span').show();
	    }
	};
        //con_descon();
        anexo_acordeon();
	//para el estado de Conexion
        $(window).resize(function() {
            adecuar_modal();
            ocultar_hiddenconboton();
        });
    });

    //Boton conectar y desconectar
    function con_descon(){
        var butt = document.getElementsByClassName("onyoff");
        var k;

        for (k = 0; k < butt.length; k++) {
            butt[k].onclick = function() {
                var asdf = $(this);
                if(asdf.hasClass('button-success')){
                    this.classList.add("pure-button-disabled");
                    this.classList.toggle("active");
                    var gif = this.firstChild;
                    gif.style.display = "block";
                    var textin = this.lastChild;
                    textin.style.display = "none";
                    var intervalo = setTimeout(boton_apagar, 3000);
                    this.classList.remove("active");
                }
                if(asdf.hasClass('button-error')){
                    this.classList.add("pure-button-disabled");
                    this.classList.toggle("active");
                    var giff = this.firstChild;
                    giff.style.display = "block";
                    var textinn = this.lastChild;
                    textinn.style.display = "none";
                    var intervaloo = setTimeout(boton_prender, 3000);
                    this.classList.remove("active");
                }
            }
        }
    }

    function boton_apagar(){
        $('#header-conectar').removeClass('button-success');
        $('#header-conectar').removeClass('pure-button-disabled');
        $('#header-conectar').addClass('button-error');
        $('#desc-span').swap('#conectar-span');
        $('#iconocargando').hide();
        $('#desc-span').show();
    }

    function boton_prender(){
        $('#header-conectar').removeClass('button-error');
        $('#header-conectar').removeClass('pure-button-disabled');
        $('#header-conectar').addClass('button-success');
        $('#conectar-span').swap('#desc-span');
        $('#iconocargando').hide();
        $('#conectar-span').show();
    }

    //Ventana modal estado del dron

    function adecuar_modal(){
        var hcon = document.getElementsByClassName("hiddencon");
        var i;
	var hconl = document.getElementsByClassName("hiddencon-label");
	var m;
        if (screen.width<959) {
            for (i = 0; i < hcon.length; i++) {
                hcon[i].style.right = "-165px"
                hcon[i].style.opacity = ".8";
		var pru = hcon[i];
		for (m = 0; m < hconl.length; m++){
                    hconl[m].onclick = function(){
			/* Toggle between adding and removing the "active" class,
			   to highlight the button that controls the panel */
			if (screen.width<959){
                            this.classList.toggle("active");

                            /* Toggle between hiding and showing the active panel */
                            if (pru.style.right === "0px") {
				pru.style.right = "-165px";
				pru.style.opacity = ".8";
				this.style.display = "inline-block";
                            } else {
				pru.style.right = "0px";
				pru.style.opacity = "1";
				this.style.display = "none";
                            }
			}
                    }
		}
            } 
        } else if (screen.width>=959){
            for (i = 0; i < hcon.length; i++) {
                hcon[i].style.right = "0px";
                hcon[i].style.opacity = "1";
            }
        }
    }

    function ocultar_hiddenconboton(){
        var bot = document.getElementsByClassName("hiddencon-label");
        var j;
        if (screen.width<959) {
            for (j = 0; j < bot.length; j++) {
                bot[j].style.display = "inline-block";
            } 
        } else if (screen.width>=959){
            for (j = 0; j < bot.length; j++) {
                bot[j].style.display = "none";
            }
        }
    }

    //Normalizador del acordeon

    function anexo_acordeon(){
        var acc = document.getElementsByClassName("desplegable");
        var l;

        for (l = 0; l < acc.length; l++) {
            acc[l].onclick = function() {
                this.classList.toggle("active");
                var panel = this.nextElementSibling;
                if (panel.style.maxHeight){
                    panel.style.maxHeight = null;
                } else {
                    panel.style.maxHeight = panel.scrollHeight + "px";
                }
            }
        }
    }

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
}(this, this.document));
