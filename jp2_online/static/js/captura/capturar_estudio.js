$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});
	
$("#next_section_button").on('click', function(e){
	$("#parentForm").append('<input name="next" value="1">')
	// e.preventDefault();
});

$("#previous_section_button").on('click', function(e){
	$("#parentForm").append('<input name="previous" value="1">')
	// e.preventDefault();
});

(function( capturar_estudio_dynamic_form, $, undefined ) {

    function append_anwser(id_question, response) {
		
		var id = $(response).attr('id').replace(/\D/g,'');
		var div = '<div class="form-container"><div class="item form-group"><div class="col-md-6 col-sm-6 col-xs-12"><div class="col-sm-12"><p>';
		
		div += response;
		div += '</p></div></div><div class="col-xs-12 col-sm-12 col-md-3 col-lg-3"><a id="delete-for-' 
		div += id + '"';
		div += ' class="btn btn-danger delete-answer" href="javascript:void(0)">-</a></div></div></div>'

		$("#question-container-" + id_question).append(div);
	}

    $(document).on('click', '.delete-answer', (function(sender) {
		var id_respuesta = $(sender.target).attr('id').replace(/\D/g,'');
		
		$.ajax({
			url : capturar_estudio_dynamic_form.url_remove_answer,

			method : "POST",

			data : {"id_respuesta" : id_respuesta},

			success : function(response) {
				$(sender.target).closest("div.form-container").remove()
			}
		});

	}));

	$('.add-answer').click(function() {

		var id_question = $(this).attr('id').replace(/\D/g,'');
		$.ajax({
			url : capturar_estudio_dynamic_form.url_add_answer,

			method : "POST",

			data : {"id_estudio" : capturar_estudio_dynamic_form.id_study, "id_pregunta" : id_question},

			success : function(response) {
				append_anwser(id_question, response)
			}
		});
	});

	capturar_estudio_dynamic_form.init = function(parameters) {
		capturar_estudio_dynamic_form.url_add_answer = parameters.url_add_answer;
		capturar_estudio_dynamic_form.url_remove_answer = parameters.url_remove_answer;
		capturar_estudio_dynamic_form.id_study = parameters.id_study;
	}

}( window.capturar_estudio_dynamic_form = window.capturar_estudio_dynamic_form || {}, jQuery ));
