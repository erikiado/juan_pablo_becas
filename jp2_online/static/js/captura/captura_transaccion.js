console.log('saludos')
function changeSubmitToAjax(id_modal, id_form) {
  console.log(id_form)
  $(id_form).submit(function(e){
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
  // hide inputs from creation form
  // change to ajax
  changeSubmitToAjax('#modal_create_egreso', '#form-create-egreso');
  changeSubmitToAjax('#modal_create_ingreso', '#form-create-ingreso');
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

function initEditForm() {
  changeSubmitToAjax('#modal_update_transaccion', '#form-edit-transaccion');
}

$(".update_transaccion_link").click(function(ev) { // for each edit contact url
  ev.preventDefault(); // prevent navigation
  var url = $(this).data("form"); // get the contact form url
  $("#modal_update_transaccion_content").load(url, function() { // load the url into the modal
      $("#modal_update_transaccion").modal('show'); // display the modal on url load
      initEditForm();
  });
  return false; // prevent the click propagation
});