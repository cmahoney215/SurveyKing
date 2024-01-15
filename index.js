const topmenu = document.querySelector('#home-list');
const menu = document.querySelector('#home-list-items');

topmenu.addEventListener('click', function() {
if (menu.classList.contains('hidden')) {
    menu.classList.remove('hidden');
}
else {
    menu.classList.add('hidden');
}
});
