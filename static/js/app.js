const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const colorPicker = document.getElementById('colorPicker');
const cooldownMsg = document.getElementById('cooldownMsg');
const colors = ['#FFFFFF', '#000000', '#FF0000', '#00FF00', '#0000FF'];
let canPlace = true;

function drawCanvas(data) {
    for (let y = 0; y < 128; y++) {
        for (let x = 0; x < 128; x++) {
            ctx.fillStyle = colors[data[y][x]];
            ctx.fillRect(x, y, 1, 1);
        }
    }
}

canvas.addEventListener('click', function(event) {
    if (!canPlace) return;
    const x = Math.floor(event.offsetX);
    const y = Math.floor(event.offsetY);
    const color = parseInt(colorPicker.value);
    fetch('/update_pixel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x, y, color })
    }).then(() => {
        loadCanvas();
        canPlace = false;
        cooldownMsg.textContent = "Cooldown: 30s";
        let countdown = 30;
        const interval = setInterval(() => {
            countdown--;
            cooldownMsg.textContent = `Cooldown: ${countdown}s`;
            if (countdown <= 0) {
                clearInterval(interval);
                canPlace = true;
                cooldownMsg.textContent = "";
            }
        }, 1000);
    });
});

function loadCanvas() {
    fetch('/get_canvas')
        .then(res => res.json())
        .then(data => drawCanvas(data));
}

loadCanvas();