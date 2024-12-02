const gameArea = document.getElementById('game-area');
const instructions = document.getElementById('instructions');
const scoreDisplay = document.getElementById('score');
const restartButton = document.getElementById('restart-button');
const tank = document.createElement('div');
tank.classList.add('tank');
tank.style.left = '375px';
tank.style.top = '550px';
gameArea.appendChild(tank);

let tankX = 375;
let tankY = 550;
let bullets = [];
let enemies = [];
let score = 0;
let keys = {};
const maxEnemies = 100;
let enemyCount = 0;
let gamePaused = false;

function createEnemy() {
    if (enemyCount >= maxEnemies || gamePaused) return;

    const enemy = document.createElement('div');
    enemy.classList.add('enemy');
    const x = Math.random() * (800 - 30);
    const y = Math.random() * (300 - 30);
    enemy.style.left = `${x}px`;
    enemy.style.top = `${y}px`;
    gameArea.appendChild(enemy);
    enemies.push(enemy);
    enemyCount++;
}

function moveTank(dx, dy) {
    if (gamePaused) return;

    tankX += dx;
    tankY += dy;
    tank.style.left = `${tankX}px`;
    tank.style.top = `${tankY}px`;

    // 边界检测
    if (tankX < 0) tankX = 0;
    if (tankX > 750) tankX = 750;
    if (tankY < 0) tankY = 0;
    if (tankY > 550) tankY = 550;
}

function shoot() {
    if (gamePaused) return;

    const bullet = document.createElement('div');
    bullet.classList.add('bullet');
    bullet.style.left = `${tankX + 22.5}px`;
    bullet.style.top = `${tankY - 10}px`;
    gameArea.appendChild(bullet);
    bullets.push(bullet);

    function moveBullet() {
        if (gamePaused) return;

        let bulletY = parseFloat(bullet.style.top);
        bulletY -= 10;
        bullet.style.top = `${bulletY}px`;

        if (bulletY < 0) {
            gameArea.removeChild(bullet);
            bullets.splice(bullets.indexOf(bullet), 1);
            return;
        }

        for (let i = 0; i < enemies.length; i++) {
            const enemy = enemies[i];
            const enemyRect = enemy.getBoundingClientRect();
            const bulletRect = bullet.getBoundingClientRect();

            if (bulletRect.left < enemyRect.right &&
                bulletRect.right > enemyRect.left &&
                bulletRect.top < enemyRect.bottom &&
                bulletRect.bottom > enemyRect.top) {
                gameArea.removeChild(enemy);
                gameArea.removeChild(bullet);
                enemies.splice(i, 1);
                bullets.splice(bullets.indexOf(bullet), 1);
                enemyCount--;
                score += 1000;
                scoreDisplay.innerText = `Score: ${score}`;
                break;
            }
        }

        requestAnimationFrame(moveBullet);
    }

    requestAnimationFrame(moveBullet);
}

document.addEventListener('keydown', (e) => {
    if (gamePaused) return;

    keys[e.key] = true;

    if (keys['w'] && keys['a']) {
        moveTank(-5, -5);
    } else if (keys['w'] && keys['d']) {
        moveTank(5, -5);
    } else if (keys['s'] && keys['a']) {
        moveTank(-5, 5);
    } else if (keys['s'] && keys['d']) {
        moveTank(5, 5);
    } else if (keys['w']) {
        moveTank(0, -10);
    } else if (keys['s']) {
        moveTank(0, 10);
    } else if (keys['a']) {
        moveTank(-10, 0);
    } else if (keys['d']) {
        moveTank(10, 0);
    }

    if (e.key === ' ') {
        shoot();
    }
});

document.addEventListener('keyup', (e) => {
    delete keys[e.key];
});

setInterval(createEnemy, 2000);

function checkScore() {
    if (score >= 10000000000) {
        gamePaused = true;
        fetch('game.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `score=${score}`
        }).then(response => response.text())
          .then(data => {
              alert(data);
              // 游戏暂停后停止所有活动
              bullets.forEach(bullet => gameArea.removeChild(bullet));
              enemies.forEach(enemy => gameArea.removeChild(enemy));
              bullets = [];
              enemies = [];
              enemyCount = 0;
          });
    }
}

setInterval(checkScore, 1000);

restartButton.addEventListener('click', () => {
    score = 0;
    gamePaused = false;
    scoreDisplay.innerText = `Score: ${score}`;
    bullets.forEach(bullet => gameArea.removeChild(bullet));
    enemies.forEach(enemy => gameArea.removeChild(enemy));
    bullets = [];
    enemies = [];
    enemyCount = 0;
    tankX = 375;
    tankY = 550;
    tank.style.left = `${tankX}px`;
    tank.style.top = `${tankY}px`;
});