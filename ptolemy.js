function padLeft(nr, n, str) {
	return Array(n-String(nr).length+1).join(str||'0')+nr;
}

function toSexigesimal(decimal) {
	var degrees = Math.floor(decimal);
	var minutes = Math.floor((decimal - degrees) * 60);
	var seconds = Math.floor((((decimal - degrees) * 60) - minutes) * 60);
	return degrees + "°" + padLeft(minutes, 2) + "'" + padLeft(seconds, 2) + '"';
}

function toDecimal(n) {
	var array = n.split("°").join(',').split("'").join(',').split('"').join(',').split(',');
	var result = parseInt(array[0]);
	result += parseInt(array[1]) / 60;
	result += parseInt(array[2]) / 3600;
	return result;
}

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
	}
}

function calcDecimal() {
	var sexigesimalInput = document.getElementById('sexigesimal').value;
	// How do I achieve the same eval() flexibility for the sexigesimal input?

	// man, Sublime is not handling this regex well - it forgets everything else is not a quote
	var sanitized = sexigesimalInput.replace(/[^0-9.+-/*\°\'\"]/gi, '');
	var result = toDecimal(sanitized);
	console.log(result);

	// whoops, turns out NaN == NaN is still false.
	if (isNaN(result)) {
		document.getElementById("sexigesimal").className = 'form-group-has-warning';
	} else {
		document.getElementById('decimal').value = result;
	}
}