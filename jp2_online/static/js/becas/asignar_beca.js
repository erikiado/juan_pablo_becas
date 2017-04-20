$(document).ready(function() {
  recalculate();
});

$('#id_tabulador').change(function() {
  recalculate();
});

$('#id_porcentaje').change(function() {
  setAportacion(parseFloat($(this).val()));
});


function setAportacion(percentage) {
  var aportacion = (1500. - 1500.*percentage/100.).toFixed(2);
  $('#id_monto').html(aportacion);
}

function setPercentage(val) {
  $('#id_porcentaje').val(val.toString());
}

/*
this function sets the percentage and amount to pay
given the current tabulador, according to the
table provided.
*/
function recalculate() {
  var tabulador;
  if ($('#id_tabulador').val() == '20_percent') {
    tabulador = tabuladorVeinte;
  }
  else if ($('#id_tabulador').val() == '14_percent') {
    tabulador = tabuladorCatorce;
  }
  var ingreso = parseFloat($('#id_ingresos').html());
  for (var i = 0; i < tabulador.length; i++) {
    if (ingreso < tabulador[i].upperLim) {
      setAportacion(tabulador[i].percentage);
      setPercentage(tabulador[i].percentage);
      break;
    }
  }
}

/*
helper function to construct a custom object
to represent the table of ranges. we save the upper limit
of the current range, and the percentage given for
that range, according to the Excel provided.
*/
function createRange(lim, perc) {
  return {
    'upperLim': lim,
    'percentage': perc
  };
}

// tabulador for 14%
var tabuladorCatorce = [
  createRange(750, 100),
  createRange(900, 93),
  createRange(1200, 90),
  createRange(1500, 87),
  createRange(1900, 83),
  createRange(2300, 80),
  createRange(2600, 77),
  createRange(3000, 73),
  createRange(3300, 70),
  createRange(3700, 67),
  createRange(4100, 63),
  createRange(4400, 60),
  createRange(4800, 57),
  createRange(5100, 53),
  createRange(5400, 50),
  createRange(5800, 47),
  createRange(6200, 43),
  createRange(6600, 40),
  createRange(7300, 33),
  createRange(8000, 27),
  createRange(8300, 20),
  createRange(9400, 13),
  createRange(10000, 7),
  createRange(10000000000000, 0) // dummy infinity for convenience
]

// tabulador for 20%
var tabuladorVeinte = [
  createRange(500, 100),
  createRange(750, 93),
  createRange(850, 90),
  createRange(1100, 87),
  createRange(1300, 83),
  createRange(1550, 80),
  createRange(1800, 77),
  createRange(2050, 73),
  createRange(2300, 70),
  createRange(2550, 67),
  createRange(2800, 63),
  createRange(3050, 60),
  createRange(3300, 57),
  createRange(3550, 53),
  createRange(3800, 50),
  createRange(4050, 47),
  createRange(4300, 43),
  createRange(4550, 40),
  createRange(5050, 33),
  createRange(5550, 27),
  createRange(6050, 20),
  createRange(6550, 13),
  createRange(7050, 7),
  createRange(10000000000000, 0) // dummy infinity for convenience
]