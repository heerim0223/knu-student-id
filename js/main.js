document.addEventListener('DOMContentLoaded', () => {
    const card = document.getElementById('card');
    const shine = document.getElementById('shine');
    let isDown = false;
    let startX, startY, rotX = 0, rotY = 0;
    let velX = 0, velY = 0;
    let lastX, lastY;
    let animId;

    function setTransform(rx, ry) {
        rotX = Math.max(-30, Math.min(30, rx));
        rotY = Math.max(-35, Math.min(35, ry));
        card.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`;

        const sx = 50 + rotY * 1.2;
        const sy = 50 - rotX * 1.2;
        shine.style.background = `radial-gradient(circle at ${sx}% ${sy}%, rgba(255,255,255,0.18) 0%, transparent 65%)`;
    }

    card.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = lastX = e.clientX;
        startY = lastY = e.clientY;
        velX = velY = 0;
        cancelAnimationFrame(animId);
        card.style.transition = 'none';
        e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDown) {
        const rect = card.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        const dx = e.clientX - cx;
        const dy = e.clientY - cy;
        if (Math.sqrt(dx*dx + dy*dy) < 180) {
            setTransform(-dy * 0.05, dx * 0.05);
        }
        return;
        }

        velX = e.clientX - lastX;
        velY = e.clientY - lastY;
        lastX = e.clientX;
        lastY = e.clientY;

        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        setTransform(rotX - dy * 0.4, rotY + dx * 0.4);
        startX = e.clientX;
        startY = e.clientY;
    });

    document.addEventListener('mouseup', () => {
        if (isDown) {
        isDown = false;
        inertia();
        }
    });

    function inertia() {
        velX *= 0.88;
        velY *= 0.88;
        setTransform(rotX - velY * 0.3, rotY + velX * 0.3);

        if (Math.abs(velX) > 0.2 || Math.abs(velY) > 0.2) {
        animId = requestAnimationFrame(inertia);
        } else {
        springBack();
        }
    }

    function springBack() {
        function step() {
        rotX *= 0.85;
        rotY *= 0.85;
        setTransform(rotX, rotY);
        if (Math.abs(rotX) > 0.3 || Math.abs(rotY) > 0.3) {
            requestAnimationFrame(step);
        } else {
            setTransform(0, 0);
        }
        }
        requestAnimationFrame(step);
    }

    card.addEventListener('touchstart', (e) => {
        const t = e.touches[0];
        isDown = true;
        startX = lastX = t.clientX;
        startY = lastY = t.clientY;
        velX = velY = 0;
        cancelAnimationFrame(animId);
        card.style.transition = 'none';
    }, { passive: true });

    card.addEventListener('touchmove', (e) => {
        const t = e.touches[0];
        velX = t.clientX - lastX;
        velY = t.clientY - lastY;
        lastX = t.clientX;
        lastY = t.clientY;

        const dx = t.clientX - startX;
        const dy = t.clientY - startY;
        setTransform(rotX - dy * 0.4, rotY + dx * 0.4);
        startX = t.clientX;
        startY = t.clientY;
        e.preventDefault();
    }, { passive: false });

    card.addEventListener('touchend', () => {
        isDown = false;
        inertia();
    });

    document.getElementById('applyBtn').addEventListener('click', applyAll);

    function applyAll() {
        const nameInput = document.getElementById('nameInput').value.trim();
        const deptInput = document.getElementById('deptInput').value.trim();

        if (nameInput) {
        const words = nameInput.split(' ');
        document.getElementById('cardName').innerHTML = 
            words.length >= 2 ? words[0] + '<br>' + words.slice(1).join(' ') : nameInput;
        }

        if (deptInput) {
        document.getElementById('cardDept').textContent = deptInput;
        }
    }

    document.getElementById('nameInput').addEventListener('keydown', e => {
        if (e.key === 'Enter') applyAll();
    });
    document.getElementById('deptInput').addEventListener('keydown', e => {
        if (e.key === 'Enter') applyAll();
    });
});