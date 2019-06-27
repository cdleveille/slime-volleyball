// http-server -a localhost -p 8000 -c-1    http://localhost:8000/index.html

import Ball from '/src/ball.js';
import Game from '/src/game.js';

let canvas = document.getElementById("gameScreen");
let ctx = canvas.getContext('2d');

const GAME_WIDTH = canvas.width;
const GAME_HEIGHT = canvas.height;

//let p1 new Player(...);
//let p2 new Player(...);

let game = new Game(GAME_WIDTH, GAME_HEIGHT, new Ball(24), 0.6, 0.98);
                //  gameWidth, gameHeight, ball, gravity, bounce

let lastTime = 0;
function gameLoop(timestamp) {

    let deltaTime = timestamp - lastTime;
    lastTime = timestamp;

    ctx.clearRect(0, 0, GAME_WIDTH, GAME_HEIGHT);

    game.update();

    game.handleCollisions();

    game.draw(ctx);

    requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);