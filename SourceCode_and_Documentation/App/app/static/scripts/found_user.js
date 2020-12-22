function showModal(id) {
    const popup = document.getElementById(`popup-${id}`);
    // Delay so it fires after window.onclick
    setTimeout(() => { popup.classList.toggle('show') }, 5);
}

function modalNavigate(url) {
    location.href = url;
}

window.onclick = () => {
    const popups = document.getElementsByClassName('popuptext');
    for(let i = 0; i < popups.length; ++i)
        if (popups[i].classList.contains('show'))
            popups[i].classList.remove('show');
};
