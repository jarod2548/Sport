const dayCheckBoxes= document.querySelectorAll('.showDay');

const dayClasses = ['addInputMonday', 'addInputTuesday', 'addInputWednesday', 'addInputThursday', 'addInputFriday', 'addInputSaturday', 'addInputSunday'];
const timeClasses = ['addOchtend', 'addMiddag', 'addAvond']

const planningElement = document.querySelector(".planning");
const saveProfile = document.querySelector(".saveProfile")

function savePlanning(event){
    let inputTexts = document.querySelectorAll('input[type = "text"]');
    let values = '';
    let classes = '';
    inputTexts.forEach((input, index) => {
       values +=  `${input.value},`;
       classes += `${input.classList},`;
    });
    values = values.slice(0, -1);
    classes = classes.slice(0, -1);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/savePlanning", true);

    var formData = new FormData();
    formData.append("vals", values);
    formData.append("classes", classes);

    xhr.send(formData)
}

document.addEventListener("DOMContentLoaded", function(){
    planningElement.addEventListener("click", function(event) {
      // Check if the clicked element is the button
      if (event.target && dayClasses.some(dayClass => event.target.classList.contains(dayClass))) {
        let td = event.target.closest("td"); // Get the <td> where the button was clicked

        // Create a new input element
        let input = document.createElement("input");
        input.type = "text"; // You can change the type if needed
        input.placeholder = "Voer oefening toe"; // Optional placeholder text
        let dayClass = dayClasses.find(day => event.target.classList.contains(day)).replace('addInput', '');
        let timeClass = timeClasses.find(time => event.target.classList.contains(time)).replace('add', '')
        input.classList.add(dayClass); // Add the corresponding class (Monday or Tuesday)
        input.classList.add(timeClass)

        // Clear existing text (if any) and append the input
        td.appendChild(input); // Append the input field to the <td>
      }
    });
});




dayCheckBoxes.forEach(checkbox => {

    const input = document.getElementById(checkbox.getAttribute('data-target'));
    if (checkbox.checked) {
        input.style.display = '';
      } else {
        input.style.display = 'none';
    }

    checkbox.addEventListener('change', function(){
        if (checkbox.checked) {
        input.style.display = '';
      } else {
        input.style.display = 'none';
    }
    });
});
