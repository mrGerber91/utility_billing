document.addEventListener('DOMContentLoaded', () => {
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    if ($navbarBurgers.length > 0) {
        $navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {
                const target = el.dataset.target;
                const $target = document.getElementById(target);
                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');
            });
        });
    }

    // Change background image and animation based on the time of day
    const hours = new Date().getHours();
    const navbar = document.querySelector('.navbar');
    const footer = document.querySelector('.footer');
    const hero = document.querySelector('.hero');

    if (hours >= 6 && hours < 20) {
        document.body.style.backgroundImage = "url('https://s3.timeweb.cloud/a43db249-billing/white.webp')";
        navbar.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
        footer.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
        navbar.style.color = 'black';
        footer.style.color = 'black';
        hero.classList.add('hero-day');
        hero.classList.remove('hero-night');
    } else {
        document.body.style.backgroundImage = "url('https://s3.timeweb.cloud/a43db249-billing/black.webp')";
        navbar.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        footer.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        navbar.style.color = 'white';
        footer.style.color = 'white';
        hero.classList.add('hero-night');
        hero.classList.remove('hero-day');
    }
});
