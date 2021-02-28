const textEl = document.getElementById('main-bio');
const avatarEl = document.getElementById("avatar");

textEl.addEventListener('input', resizeArea)
textEl.addEventListener("keypress", submitOnEnter);

avatarEl.addEventListener('change', () => avatarEl.form.submit());
resizeArea();

function submitOnEnter(event) {
    if (event.which === 13 && !event.shiftKey){
        event.preventDefault();
        textEl.form.submit();
    }
}

function resizeArea() {
    textEl.style.height = 'auto';
    textEl.style.height = textEl.scrollHeight + 'px';
}