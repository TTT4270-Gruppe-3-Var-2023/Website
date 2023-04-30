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