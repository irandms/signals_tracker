function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    if(h == 15 && m < 50) {
      var average = document.getElementById('total').innerHTML / (m + s/60);
      document.getElementById('average').innerHTML = average;
    }
    else if(h != 15) {
     	var average = document.getElementById('total').innerHTML / (50);
      	document.getElementById('average').innerHTML = average;
    }
    var t = setTimeout(startTime, 500);
}
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}
