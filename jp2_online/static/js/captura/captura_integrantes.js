$(document).ready(function() {
  $('#tablaCapturista').dataTable();
  $('#id_fecha_de_nacimiento').datepicker({
    changeMonth: true,
    changeYear: true}
  );
  $("#_id_escuela").hide();
  $("#_id_numero_sae").hide();
  $("#_id_relacion").hide();
});

// using jQuery
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});


// hide or show certain fields based on the rol
$('#id_rol').change(function(e) {
  if (e.target.value == 'tutor') {
    $("#_id_escuela").hide();
    $("#_id_numero_sae").hide();
    $("#_id_relacion").show();
  }
  else if (e.target.value == 'alumno') {
    $("#_id_escuela").show();
    $("#_id_numero_sae").show();
    $("#_id_relacion").hide();
  }
  else if (e.target.value == 'ninguno') {
    $("#_id_escuela").hide();
    $("#_id_numero_sae").hide();
    $("#_id_relacion").hide();
  }
})

$(document).ready(function() {
  // send form via ajax
  $("#form-create-integrante").submit(function(e){
    e.preventDefault();
    $.ajax({ 
      type: $(this).attr('method'), 
      url: this.action, 
      data: $(this).serialize(),
      context: this,
      success: function(data, status_code) {
        $('#modal_create_integrante').modal('toggle'); // close modal
        swal({
          title: 'Integrante Creado',
          type: 'success',
          confirmButtonText: 'OK',
        }).then(function (isConfirm) {
          if (isConfirm) {
            location.reload(); // reload page after closing
          }
        });
      },
      error: function(data, status_code) {
        swal({
          title: 'Error!',
          text: data.responseJSON[Object.keys(data.responseJSON)[0]][0].message, // obtain first error msg
          type: 'error',
          confirmButtonText: 'OK'
        });
      }
    });
  });
})
