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

window.addEventListener("DOMContentLoaded", () => {
    // Creates a websocket connection to the port 5678
    const websocket = new WebSocket("ws://localhost:5678/");
    
    // Upon reception of a package, it turns it from JSON to JS-object, updates the statuses and sets the background-color accordingly
    websocket.onmessage = ({ data }) => {
        const statuses_obj = JSON.parse(data);
        
        for (let statuses_key in statuses_obj) {
            document.getElementById(statuses_key).innerHTML = statuses_obj[statuses_key];
            
            if (statuses_obj[statuses_key] == "0") {
                document.getElementById(statuses_key).style.backgroundColor = "red";
            } else {
                document.getElementById(statuses_key).style.backgroundColor = "green";
            }
        }  
    };
});