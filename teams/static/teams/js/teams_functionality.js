let joinTeamField = document.getElementById('id_identifier');
let createTeamField = document.getElementById('id_title');

console.log(joinTeamField)
console.log(createTeamField);

joinTeamField.addEventListener('keypress', function submitOnEnter(event) {
    if (event.which === 13){
        event.form.submit();
    }
})