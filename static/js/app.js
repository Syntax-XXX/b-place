const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const cooldownMsg = document.getElementById('cooldownMsg');
const colorPicker = document.getElementById('colorPicker');
let currentColor = 1;
let canPlace = true;
const scaleFactor = 2;
const x = Math.floor((event.clientX - rect.left) * (canvas.width / canvas.offsetWidth) / scaleFactor);
const y = Math.floor((event.clientY - rect.top) * (canvas.height / canvas.offsetHeight) / scaleFactor);


canvas.style.width = "1000px";
canvas.style.height = "1000px";
ctx.imageSmoothingEnabled = false;
ctx.scale(2, 2);  // Make each pixel render as 2×2

const colors = [
    '#FFFFFF', '#000000', '#FF0000', '#FFA500', '#FFFF00',
    '#008000', '#00FFFF', '#0000FF', '#800080', '#FFC0CB', '#A52A2A'
];

colors.forEach((color, i) => {
    const box = document.createElement('div');
    box.className = 'color-box';
    box.style.backgroundColor = color;
    if (i === currentColor) box.classList.add('selected');
    box.addEventListener('click', () => {
        document.querySelectorAll('.color-box').forEach(b => b.classList.remove('selected'));
        box.classList.add('selected');
        currentColor = i;
    });
    colorPicker.appendChild(box);
});

canvas.addEventListener('click', function(event) {
    if (!canPlace) return;
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((event.clientX - rect.left) * canvas.width / rect.width);
    const y = Math.floor((event.clientY - rect.top) * canvas.height / rect.height);

    fetch('/update_pixel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x, y, color: currentColor })
    }).then(res => {
        if (res.status === 200) {
            loadCanvas();
            startCooldown();
        } else {
            res.text().then(alert);
        }
    });
});

function startCooldown() {
    canPlace = false;
    cooldownMsg.textContent = "Cooldown: 30s";
    let countdown = 30;
    const interval = setInterval(() => {
        countdown--;
        cooldownMsg.textContent = `Cooldown: ${countdown}s`;
        if (countdown <= 0) {
            clearInterval(interval);
            cooldownMsg.textContent = "";
            canPlace = true;
        }
    }, 1000);
}

function loadCanvas() {
    fetch('/get_canvas')
        .then(res => res.json())
        .then(data => {
            for (let y = 0; y < canvas.height; y++) {
                for (let x = 0; x < canvas.width; x++) {
                    ctx.fillStyle = colors[data[y][x]];
                    ctx.fillRect(x, y, 1, 1); // Each logical 1x1 becomes 2x2 visually
                }
            }
        });
}

loadCanvas();
