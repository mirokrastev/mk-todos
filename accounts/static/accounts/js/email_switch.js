let parentForm = document.getElementById('formContent').children[0];

let emailField = document.getElementById('id_email').parentElement;

let toInsertBefore = parentForm.getElementsByTagName('br')[0];

function checkSwitchButton(event) {
    if (event.checked) {
        emailField.remove();
    }
    else {
        parentForm.insertBefore(emailField, toInsertBefore);
    }
}