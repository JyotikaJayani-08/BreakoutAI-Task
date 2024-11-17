// dashboard/static/dashboard/twinkle.js

document.addEventListener('DOMContentLoaded', () => {
    const createDot = () => {
        const dot = document.createElement('div');
        dot.className = 'dot';
        dot.style.top = `${Math.random() * 100}vh`;
        dot.style.left = `${Math.random() * 100}vw`;
        dot.style.animationDuration = `${Math.random() * 2 + 1}s`;
        document.body.appendChild(dot);

        setTimeout(() => {
            dot.remove();
        }, 3000);
    };

    setInterval(createDot, 500);
});