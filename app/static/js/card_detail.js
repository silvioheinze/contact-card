(function () {
    const trigger = document.querySelector('.qr-code-trigger');
    const overlay = document.getElementById('qr-code-overlay');
    if (!trigger || !overlay) {
        return;
    }

    function openOverlay() {
        overlay.hidden = false;
        trigger.setAttribute('aria-expanded', 'true');
        document.body.classList.add('qr-code-overlay-open');
    }

    function closeOverlay() {
        overlay.hidden = true;
        trigger.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('qr-code-overlay-open');
        trigger.focus();
    }

    trigger.addEventListener('click', openOverlay);
    overlay.addEventListener('click', closeOverlay);

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && !overlay.hidden) {
            closeOverlay();
        }
    });
})();
