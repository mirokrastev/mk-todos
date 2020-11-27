const textEl = document.getElementById('main-bio');
const avatarEl = document.getElementById("avatar");

textEl.setAttribute("oninput", "resizeArea();");
textEl.addEventListener("keypress", submitOnEnter);

avatarEl.setAttribute('onchange', 'form.submit();');

resizeArea();

function submitOnEnter(event) {
    if (event.which === 13 && !event.shiftKey){
        event.target.parentElement.submit();
        event.preventDefault();
    }
}

function resizeArea() {
    textEl.style.height = 'auto';
    textEl.style.height = textEl.scrollHeight + 'px';
}
