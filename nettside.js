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
    const websocket = new WebSocket("ws://192.168.43.206:5678");
    
    // Upon reception of a package, it turns it from JSON to JS-object, updates the statuses and sets the background-color accordingly
    websocket.onmessage = ({ data }) => {
        const statuses_obj = JSON.parse(data);
        
        let groupedData = {};

        for (let key in statuses_obj) {
        let prefix = key.split("_")[0];
        if (!groupedData[prefix]) {
        groupedData[prefix] = [];
        }
        groupedData[prefix].push(key);
        }
        for (let group_key in groupedData){
            if (group_key == "mens"){
                for (let i = 0; i < groupedData[group_key].length; i++) {
                    //update div 
                    let current_key = groupedData[group_key][i]
                    let custom_inner_HTML = '<img class="img-fluid icon" src="figures/Toilets_male.svg" style="height: 80%; padding: 0; margin: 0;" alt="Mens Toilet"><p style="padding: 1%; margin: 1%;">'
                    document.getElementById(current_key).innerHTML = custom_inner_HTML + statuses_obj[current_key] + "/3</p>";
                    if (statuses_obj[current_key] == "0") {
                        document.getElementById(current_key).style.backgroundColor = "red";
                    }
                    else if (statuses_obj[current_key] == "1") {
                        document.getElementById(current_key).style.backgroundColor = "orange";
                    }
                    else {
                        document.getElementById(current_key).style.backgroundColor = "green";
                    }
                    
                    
                    // alert("  " + groupedData[group_key][i]);
                  }
                
            }
            else if (group_key == "ladies"){
                for (let i = 0; i < groupedData[group_key].length; i++) {
                    //update div 
                    let current_key = groupedData[group_key][i]
                    let custom_inner_HTML = '<img class="img-fluid icon" src="figures/Toilets_female.svg" style="height: 80%; padding: 0; margin: 0;" alt="Ladies Toilet"><p style="padding: 1%; margin: 1%;">'
                    document.getElementById(current_key).innerHTML = custom_inner_HTML + statuses_obj[current_key] + "/3</p>";
                    if (statuses_obj[current_key] == "0") {
                        document.getElementById(current_key).style.backgroundColor = "red";
                    }
                    else if (statuses_obj[current_key] == "1") {
                        document.getElementById(current_key).style.backgroundColor = "orange";
                    }
                    else {
                        document.getElementById(current_key).style.backgroundColor = "green";
                    }
                    
                    
                    // alert("  " + groupedData[group_key][i]);
                  }
                
            }
            else if (group_key == "handicap"){
                for (let i = 0; i < groupedData[group_key].length; i++) {
                    //update div 
                    let current_key = groupedData[group_key][i]
                    let custom_inner_HTML = '<img class="img-fluid icon" src="figures/Toilets_handicap.svg" style="height: 80%; padding: 0; margin: 0;" alt="Handicap Toilet"><p style="padding: 1%; margin: 1%;">'
                    document.getElementById(current_key).innerHTML = custom_inner_HTML + statuses_obj[current_key] + "/1</p>";
                    if (statuses_obj[current_key] == "0") {
                        document.getElementById(current_key).style.backgroundColor = "red";
                    }
                    else if (statuses_obj[current_key] == "1") {
                        document.getElementById(current_key).style.backgroundColor = "orange";
                    }
                    else {
                        document.getElementById(current_key).style.backgroundColor = "green";
                    }
                    
                    
                    // alert("  " + groupedData[group_key][i]);
                  }
                
            }
            else if (group_key == "bar"){
                for (let i = 0; i < groupedData[group_key].length; i++) {
                    //update div 
                    let current_key = groupedData[group_key][i]
                    let custom_inner_HTML = '<img class="img-fluid icon" src="figures/Bar.svg" style="height: 80%; padding: 0; margin: 0;" alt="Bar"><p  style="padding: 1%; margin: 1%;">'
                    document.getElementById(current_key).innerHTML = custom_inner_HTML + statuses_obj[current_key] + " min</p>";
                    if (parseFloat( statuses_obj[current_key]) <= 4) {
                        document.getElementById(current_key).style.backgroundColor = "green";
                    }
                    else if (parseFloat( statuses_obj[current_key]) <= 8) {
                        document.getElementById(current_key).style.backgroundColor = "orange";
                    }
                    else {
                        document.getElementById(current_key).style.backgroundColor = "red";
                    }
                    
                    
                    // alert("  " + groupedData[group_key][i]);
                  }
                
            }
        }

        console.log(groupedData);

        for (let statuses_key in statuses_obj) {
            
            
        }  
    };
});