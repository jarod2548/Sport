
document.addEventListener('DOMContentLoaded', function (){
    const dayCheckBoxes= document.querySelectorAll('.showDay')

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

    const registerForm = document.querySelector('.profileCanvas');

    registerForm.addEventListener('submit', function(event) {
    let valid = true;
    dayCheckBoxes.forEach(checkbox => {
        const inputContainer = document.getElementById(checkbox.getAttribute('data-target'));
        const inputs = inputContainer.querySelectorAll('input');

        if (checkbox.checked) {
        const allFilled = Array.from(inputs).every(input => input.value.trim() !== '');
        if(!allFilled){
            valid = false; // Invalid if the input is empty
            for(var i = 0; i < inputs.length; i++){
                inputs[i].style.border = '1px solid red';
            }
            } else {
            for(var i = 0; i < inputs.length; i++){
                inputs[i].style.border = '';
            }
            }
        }

    });
    if (!valid) {
    event.preventDefault(); // Prevent form submission if validation fails
    alert('Please fill in all required fields!');
  }
});
});