const textEl = document.getElementById('main-bio');
const avatarEl = document.getElementById("avatar");

textEl.addEventListener('input', resizeArea)
textEl.addEventListener("keypress", submitOnEnter);

avatarEl.addEventListener('change', function() {this.form.submit();})
resizeArea();

function submitOnEnter(event) {
    if (event.which === 13 && !event.shiftKey){
        event.target.parentElement.submit();
        event.preventDefault();
    }
}

function resizeArea() {
    this.style.height = 'auto';
    this.style.height = textEl.scrollHeight + 'px';
}
