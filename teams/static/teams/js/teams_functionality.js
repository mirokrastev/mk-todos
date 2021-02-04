let joinTeamField = document.getElementById('id_identifier');
let createTeamField = document.getElementById('id_title');

const list = [joinTeamField, createTeamField];

list.forEach(field => {
    if (!field) return;
    field.addEventListener('keypress', function(event) {
        if (event.which === 13) {
            event.target.submit();
        }
    })
})