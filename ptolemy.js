/*
	Mathematical helper functions.
*/

function padLeft(nr, n, str) {
	return Array(n-String(nr).length+1).join(str||'0')+nr;
}

Math.radians = function(degrees) {
  return degrees * Math.PI / 180;
};

function ensureSimpleAngle(angle) {
	// If the angle is less than 0 or greater than 360, convert it to a coterminal simple angle.
	if (angle < 0) {
		angle = (360 + angle);
	}

	while (angle >= 360) {
		angle -= 360;
	}
	return angle;
}

/* 
	Conversion logic and other calculations.
*/

function toSexigesimal(decimal) {
	decimal = ensureSimpleAngle(decimal);
	// TODO: Let the user know when I've messed with their inputs.

	var degrees = Math.floor(decimal);
	var minutes = Math.floor((decimal - degrees) * 60);
	var seconds = Math.floor((((decimal - degrees) * 60) - minutes) * 60);
	return degrees + "°" + padLeft(minutes, 2) + "'" + padLeft(seconds, 2) + '"';
}

function toDecimal(sexigesimal) {
	// Sexigesimal comes as a string, so split it into its 3 parts:
	var array = sexigesimal.split("°").join(',').split("'").join(',').split('"').join(',').split(',');
	var result = parseInt(array[0]);
	result += parseInt(array[1]) / 60;
	result += parseInt(array[2]) / 3600;

	result = ensureSimpleAngle(result);
	// TODO: Let the user know when I mess with their inputs.
	return result;
}

// Ptolemy divides the circle into 120 "parts" (units) for whatever reason.
// (Who am I to question him...?)
var DIAMETER_OF_CIRCLE = 120;

function toChord(decimal) {
	var result = Math.sin(Math.radians(decimal)/2) * DIAMETER_OF_CIRCLE;
	result = ensureSimpleAngle(result);
	return result;
}

/*
	Functions for getting input and displaying output.
*/

function calcSexigesimal() {
	var decimalInput = document.getElementById("decimal").value;
	// Ex. 60.23 + 21.5 = 81*43'47".
	// Should probably sanitize this as well!!
	// Input of alert("Hi!"); says hi of course.
	var sanitized = decimalInput.replace(/[^0-9.+-/*]/gi, '');
	console.log(sanitized);
	var decimal = eval(sanitized);
	var result = toSexigesimal(decimal);

	if (result == "NaN°NaN'NaN\"") {
		// not working yet
		document.getElementById("decimal").className = 'form-group-has-warning';
	}
	else {
		document.getElementById("sexigesimal").value = result;
		calcChord();
	}
}


function calcChord() {
	var decimal = document.getElementById('decimal').value;
	var result = toChord(decimal);

	document.getElementById('chord').value = result;
}

function displayHelpText() {
	// TODO
	alert("here's some help text");
}

function calcDecimal() {
	var sexigesimalInput = document.getElementById('sexigesimal').value;
	// How do I achieve the same eval() flexibility for the sexigesimal input?

	// man, Sublime is not handling this regex well - it forgets everything else is not a quote
	var sanitized = sexigesimalInput.replace(/[^0-9.+-/*\°\'\"]/gi, '');
	var result = toDecimal(sanitized);

	// whoops, turns out NaN == NaN is still false. Thanks JS.
	if (isNaN(result)) {
		document.getElementById("sexigesimal").className = 'form-group-has-warning';
	} else {
		document.getElementById('decimal').value = result;
		calcChord();
	}
}

