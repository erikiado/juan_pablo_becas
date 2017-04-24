
function setAportacion(percentage, colegiatura) {
  var aportacion = (colegiatura - colegiatura*percentage/100.).toFixed(2);
  $('#id_monto').html(aportacion);
}

function setPercentage(val) {
  $('#id_porcentaje').val(val.toString());
}

/*
this function sets the percentage and amount to pay
given the current tabulador.
*/
function recalculateFromTabulador(colegiatura) {
  var tabulador = parseFloat($('#id_tabulador').val());
  var num_alumnos = $('#tabla_alumnos tr').length - 1;
  var income = parseFloat($('#id_ingresos').html());
  var should_pay = income * tabulador / 100. / num_alumnos;
  var perc = Math.floor((colegiatura-should_pay) / colegiatura * 100);
  setPercentage(perc);
  setAportacion(perc, colegiatura);
}

/*
this function sets the tabulador and amount to pay
given the percentage
*/
function recalculateFromPercentage(perc, colegiatura) {
  var to_pay = colegiatura * (100-perc) / 100.;
  var num_alumnos = $('#tabla_alumnos tr').length - 1;
  var total_paying = num_alumnos * to_pay;
  var income = parseFloat($('#id_ingresos').html());
  var perc_from_income = Math.floor(total_paying / income * 100);
  if (perc_from_income >= 14 && perc_from_income <= 20) {
    $('#id_tabulador').val(perc_from_income.toString());
  }
  else {
    $('#id_tabulador').val('fuera_rango');
  }
  setAportacion(perc, colegiatura);
}

/*
since the option for fuera de rango is disabled, it does not get sent when submitting.
thus, we enable it before doing so, so django does not complain
*/
jQuery(function ($) {        
  $('form').bind('submit', function () {
    $('#id_tabulador option')['7'].disabled = false;
  });
});