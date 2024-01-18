//var modal = document.getElementById("myModal");
//
//var btn = document.getElementsByClassName("myBtn")[0];
//
//var span = document.getElementsByClassName("close")[0];
//
//btn.onclick = function() {
//  modal.style.display = "block";
//}
//
//span.onclick = function() {
//  modal.style.display = "none";
//}
//
//window.onclick = function(event) {
//  if (event.target == modal) {
//    modal.style.display = "none";
//  }
//}

var modal = document.getElementById("myModal");

// Select all elements with the class "myBtn"
var btns = document.getElementsByClassName("myBtn");

var span = document.getElementsByClassName("close")[0];

// Attach click event listener to each element with the class "myBtn"
for (var i = 0; i < btns.length; i++) {
  btns[i].onclick = function() {
    modal.style.display = "block";
  }
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
