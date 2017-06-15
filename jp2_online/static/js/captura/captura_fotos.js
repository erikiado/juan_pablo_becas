$(document).ready(function() {
  $('.delete_photo').click(function(ev) { // for each edit contact url
    ev.preventDefault(); // prevent navigation
    var url = $(this).data('form'); // get the contact form url
    $('#modal_delete_foto_content').load(url, function() { // load the url into the modal
      $('#modal_delete_foto').modal('show'); // display the modal on url load
    });
    return false; // prevent the click propagation
  });
});
