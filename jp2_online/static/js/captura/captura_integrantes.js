// this function changes the submit of the form to be sent via ajax, and handles the errors.
function changeSubmitToAjax(id_modal) {
  $('.form-create-integrante').submit(function(e){
    e.preventDefault();
    $.ajax({
      type: $(this).attr('method'),
      url: this.action,
      data: $(this).serialize(),
      context: this,
      success: function(data, status_code) {
        $(id_modal).modal('toggle'); // close modal
        swal({
          title: data.msg,
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
}


$(document).ready(function() {
  $('#tablaCapturista').dataTable();
  $('#id_fecha_de_nacimiento').datepicker({
    changeMonth: true,
    changeYear: true,
    maxDate: '0',
    onSelect: function(){
      var birthday = $(this).datepicker('getDate');
      var yearsApart = new Date(new Date - birthday).getFullYear()-1970;
      if(yearsApart > 0)
        $("#id_edad").val(yearsApart);
    }
  });
  $("#id_edad").on("change paste keyup", function() {
    var edad = Number($(this).val());

    if(isNaN(edad) || edad < 0)
      return;

    var date = new Date();
    date.setFullYear( date.getFullYear() - edad );
    $("#id_fecha_de_nacimiento").datepicker('setDate', date);
  });
  // hide inputs from creation form
  $('#modal_create_integrante #_id_plantel').hide();
  $('#modal_create_integrante #_id_numero_sae').hide();
  $('#modal_create_integrante #_id_relacion').hide();
  $('#modal_create_integrante #_id_ciclo_escolar').hide();
  // change to ajax
  changeSubmitToAjax('#modal_create_integrante');
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
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
    }
  }
});


// hide or show certain fields based on the rol for the creation form
$('#modal_create_integrante #id_rol').change(function(e) {
  if (e.target.value == 'tutor') {
    $('#modal_create_integrante #_id_plantel').hide();
    $('#modal_create_integrante #_id_numero_sae').hide();
    $('#modal_create_integrante #_id_ciclo_escolar').hide();
    $('#modal_create_integrante #_id_relacion').show();
  }
  else if (e.target.value == 'alumno') {
    $('#modal_create_integrante #_id_plantel').show();
    $('#modal_create_integrante #_id_numero_sae').show();
    $('#modal_create_integrante #_id_ciclo_escolar').show();
    $('#modal_create_integrante #_id_relacion').hide();
  }
  else if (e.target.value == 'ninguno') {
    $('#modal_create_integrante #_id_plantel').hide();
    $('#modal_create_integrante #_id_numero_sae').hide();
    $('#modal_create_integrante #_id_relacion').hide();
    $('#modal_create_integrante #_id_ciclo_escolar').hide();
  }
});

/*
this is called when the edit modal is loaded.

its purpose is to hide the elements of the form related to the role,
since we can't edit the role of a created integrante.
*/
function initEditForm() {
  // hide everything
  $('#modal_edit_integrante #_id_rol').hide();
  $('#modal_edit_integrante #_id_plantel').hide();
  $('#modal_edit_integrante #_id_numero_sae').hide();
  $('#modal_edit_integrante #_id_relacion').hide();


  // show sae, plantel, or relacion depending on the role.
  if ($('#modal_edit_integrante #id_rol').val() == 'alumno') {
    $('#modal_edit_integrante #_id_plantel').show();
    $('#modal_edit_integrante #_id_numero_sae').show()
    $('#modal_create_integrante #_id_ciclo_escolar').show();
  }
  else if ($('#modal_edit_integrante #id_rol').val()  == 'tutor') {
    $('#modal_edit_integrante #_id_relacion').show();
  }
  changeSubmitToAjax('#modal_edit_integrante');
}

$('.edit-integrante-link').click(function(ev) { // for each edit contact url
  ev.preventDefault(); // prevent navigation
  var url = $(this).data('form'); // get the contact form url
  $('#modal_edit_integrante_content').load(url, function() { // load the url into the modal
    $('#modal_edit_integrante').modal('show'); // display the modal on url load
    initEditForm();
  });
  return false; // prevent the click propagation
});


$('.delete_integrante_link').click(function(ev) { // for each edit contact url
  ev.preventDefault(); // prevent navigation
  var url = $(this).data('form'); // get the contact form url
  $('#modal_delete_integrante_content').load(url, function() { // load the url into the modal
    $('#modal_delete_integrante').modal('show'); // display the modal on url load
  });
  return false; // prevent the click propagation
});
