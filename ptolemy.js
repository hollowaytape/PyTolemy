function padLeft(nr, n, str) {
	return Array(n-String(nr).length+1).join(str||'0')+nr;
}

function calculate() {
	var decimal = document.getElementById("decimal").value;
	var decimal = eval(decimal);   // security issue??? gotta sanitize this
	var degrees = Math.floor(decimal);
	var minutes = Math.floor((decimal - degrees) * 60);
	var seconds = Math.floor((((decimal - degrees) * 60) - minutes) * 60);
	
	document.getElementById("sexigesimal").value = degrees + "°" + padLeft(minutes, 2) + "'" + padLeft(seconds, 2) + '"';
}