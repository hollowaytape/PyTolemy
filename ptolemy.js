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
	angle = parseInt(angle);
	while (angle < 0) {
		console.log(angle);
		angle += 360;
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
	return result;
}

var ZODIAC = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];

function toZodiac(sexigesimal) {
	// The point of the vernal equinox is 0.
	// Ptolemy and Copernicus refer to the zodiac location of various events they talk about.
	var array = sexigesimal.split("°").join(',').split("'").join(',').split('"').join(',').split(',');
	var degrees = parseInt(array[0]);
	var minutes = parseInt(array[1]) / 60;
	var seconds = parseInt(array[2]) / 3600;

	var sign = ZODIAC[Math.floor(degrees / 30)];
	var degrees_into_sign = degrees % 30;
	return degrees_into_sign + "°" + minutes + '"' + seconds + "'" + " into " + sign;
	// TODO: Copernicus does some calculation of how procession makes the zodiac positions differ
	// between his and Ptolemy's time. Add an option to display Greek/Renaissance/Present zodiacs?
}

/*
	Functions for getting input and displaying output.
*/

function updateSexigesimal() {
	var decimalInput = document.getElementById("decimal").value;
	// Ex. 60.23 + 21.5 = 81*43'47".
	// Should probably sanitize this as well!!
	// Input of alert("Hi!"); says hi of course.
	var sanitized = decimalInput.replace(/[^0-9.+-/*]/gi, '');
	var decimal = eval(sanitized);
	var result = toSexigesimal(decimal);

	if (result == "NaN°NaN'NaN\"") {
		// not working yet
		document.getElementById("decimal").className = 'form-group-has-warning';
	}
	else {
		document.getElementById("sexigesimal").value = result;
		updateChord();
		updateZodiac();
	}
}


function updateChord() {
	var decimal = document.getElementById('decimal').value;
	decimal = ensureSimpleAngle(decimal);
	var result = toChord(decimal);

	document.getElementById('chord').value = result;
}

function updateZodiac() {
	var sexigesimal = document.getElementById('sexigesimal').value;
	var result = toZodiac(sexigesimal);

	document.getElementById('zodiac').value = result;
}

function displayHelpText() {
	// TODO
	alert("here's some help text");
}

function updateDecimal() {
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
		updateChord();
		updateZodiac();
	}
}

