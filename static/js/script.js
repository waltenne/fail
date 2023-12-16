const h1 = document.querySelector('header-banner');
function highlightLetters() {
h1.textContent = h1.textContent.replace(/[a-z]/g, function(letter) {
    if (letter === 'f' || letter === 'a' || letter === 'i' || letter === 'l') {
    return letter.toUpperCase();
    } else {
    return letter;
    }
});
}

highlightLetters();