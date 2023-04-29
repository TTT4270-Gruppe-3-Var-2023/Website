function random(start, stop) {
    return Math.round(Math.random()*(stop-start) + start);
}


function myFunction() {
    document.getElementById("btn_ladies").innerHTML = "Damedo: "+random(0,10) + " min";
    document.getElementById("btn-mens").innerHTML = "Herredo: "+random(0,10) + " min";
    document.getElementById("bar a").innerHTML = "Bar A: "+random(0,10) + " min";
}

function showToilett(){
    var div_toilet = document.getElementById("div_toilet");
    var div_bar = document.getElementById("div_bar");
    div_bar.style.display = "none";                
    div_toilet.style.display = "block";
    var div_toilets = document.getElementById("div-main-toilets");
    div_toilets.style.display = "block";                
}
function showBar(){
    var div_toilets = document.getElementById("div-main-toilets");
    div_toilets.style.display = "none";                
    var div_toilet = document.getElementById("div_toilet");
    div_toilet.style.display = "none";                
    var div_bar = document.getElementById("div_bar");
    div_bar.style.display = "block";

}
function showMale(){
    var x = document.getElementById("main-mens_toilets");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
    document.getElementById('btn-mens').classList.toggle('btn-success');
    document.getElementById('btn-mens').classList.toggle('btn-secondary');
}
function showFemale(){
    var x = document.getElementById("main-ladies_toilets");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }                
    document.getElementById('btn_ladies').classList.toggle('btn-success');
    document.getElementById('btn_ladies').classList.toggle('btn-secondary');
}
function showHandicap(){
    var x = document.getElementById("main-handicap");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }          
    document.getElementById('btn_handicap').classList.toggle('btn-success');
    document.getElementById('btn_handicap').classList.toggle('btn-secondary');
}
function showBar(){
    var x = document.getElementById("div-main-bar");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }          
    document.getElementById('btn_bar').classList.toggle('btn-success');
    document.getElementById('btn_bar').classList.toggle('btn-secondary');
}