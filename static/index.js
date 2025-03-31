// script.js





document.addEventListener("DOMContentLoaded", function () {
    const expandSidebarButton = document.getElementById('expandSidebar');
    const sidebar = document.getElementById('sidebar');

    if (expandSidebarButton){
    expandSidebarButton.addEventListener('click', function () {
        sidebar.classList.toggle("hidden");  // Toggle between hidden and visible
        sidebar.classList.toggle("visible");
    });
    }

});
function showRerror(event){
    event.preventDefault();
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/register', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    var data = {
            username: document.getElementById("Ruserinput").value,
            password: document.getElementById("Rpasswordinput").value,
            email: document.getElementById("emailinput").value
        };

    xhr.onload = function(){
        if (xhr.status === 200){
        try{
            var response = JSON.parse(xhr.responseText);
            var messageElement = document.getElementById('rError');
            if(response.message == ""){
                Lelement = document.querySelector('.loginForm');
                Relement = document.querySelector('.RegisterForm');
                Relement.style.display = 'none'
                Lelement.style.display = ''
            }
            else{
                messageElement.textContent = response.message;
            }
            } catch (error) {
                console.error('Error parsing JSON:', error);
                alert('An error occurred while processing the response.' + error);
            }
        }
    };

    xhr.send(JSON.stringify(data));
}

function updateContent(number) {
    // Send AJAX POST request to the Flask server
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/showlogin", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    
    // Handle the response from the server
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Update the content of the response from the server
            var response = xhr.responseText;
            var parts = response.split('|'); // Split the response on the pipe symbol
            for(var i = 0; i < parts.length; i+=2){
                var action = parts[i]; // 'show' or 'hide'
                var elements = parts.slice(i+1); // Elements to show or hide

            // Loop through the class names returned from Flask
                elements.forEach(function(className) {
                // Select all elements with the class name
                    var elementsToToggle = document.querySelectorAll('.' + className);

                // Toggle the display for each element
                    elementsToToggle.forEach(function(element) {
                        if (action === 'show') {
                            element.style.display = '';
                        } else if (action === 'hide') {
                            element.style.display = 'none'; // Hide the element
                        }
                    });
                });
            }



        } else {
            console.error("Error: " + xhr.status); // Log any error with the request
        }
    };

    // Send the number as data in the request body
    xhr.send("number=" + number);
}
