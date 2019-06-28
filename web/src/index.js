// http-server -a localhost -p 8000 -c-1    http://localhost:8000/index.html

import Ball from "/src/ball.js";
import Player from "/src/player.js";
import Game from "/src/game.js";

let canvas = document.getElementById("gameScreen");
let ctx = canvas.getContext("2d");

let ball = new Ball(24, '#006400');

let p1Inputs = { left: 65, right: 68, jump: 87 };
let p2Inputs = { left: 37, right: 39, jump: 38 };

let p1 = new Player("P1", 56, 5, 5, 5, p1Inputs, "#00008B", false);
let p2 = new Player("P2", 56, 5, 5, 5, p2Inputs, "#8B0000", false);

let netWidth = 20;
let netHeight = 100;
let gravity = 0.1;
let bounce = 0.98;
let bounceNet = 0.75;
let framerate = 144;

let game = new Game(ctx, canvas.width, canvas.height, "#ADD8E6", p1, p2, ball, netWidth, netHeight, "#000000", gravity, bounce, bounceNet);

if (Math.random() >= 0.5) {
    game.ball.x = game.gameWidth / 4;
} else {
    game.ball.x = game.gameWidth * 3 / 4;
}

game.resetPositions();

let lastTime = 0, deltaTime = 0;
function gameLoop(timestamp) {

    requestAnimationFrame(gameLoop);

    deltaTime = (timestamp - lastTime) / (1000 / framerate);
    lastTime = timestamp;

    game.update(deltaTime);
    game.draw();
}

requestAnimationFrame(gameLoop);