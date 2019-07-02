// http-server -a localhost -p 8000 -c-1    http://localhost:8000/index.html
// game loop:   https://codeincomplete.com/posts/javascript-game-foundations-the-game-loop/

import Ball from "/src/ball.js";
import Player from "/src/player.js";
import Game from "/src/game.js";
import WindowHandler from "/src/window.js";
import AI from "/src/ai.js";

let canvas = document.getElementById("gameScreen");
let ctx = canvas.getContext("2d");

let ball = new Ball(24, '#006400');

let playerRadius = 56;
let playerSpeed = 5;
let playerJump = 5;

let p1Inputs = { left: 65, right: 68, jump: 87 , slow: 83, toggleAI: 49 };
let p2Inputs = { left: 37, right: 39, jump: 38 , slow: 40, toggleAI: 50 };

let p1 = new Player("P1", playerRadius, playerSpeed, playerJump, p1Inputs, "#00008B", false);
let p2 = new Player("P2", playerRadius, playerSpeed, playerJump, p2Inputs, "#8B0000", true);

let scoreLimit = 10;
let netWidth = 10;
let netHeight = 100;
let gravity = 0.1;
let bounce = 0.97;
let bounceNet = 0.8;
let momentumTransfer = 0.15;

let game = new Game(scoreLimit, ctx, canvas.width, canvas.height, "#ADD8E6", p1, p2, ball, netWidth, netHeight, 
                    "#000000", gravity, bounce, bounceNet, momentumTransfer);

let ai = new AI(game);
game.p1.ai = ai;
game.p2.ai = ai;

let wh = new WindowHandler(canvas, game);
wh.resizeGameWindow();

var ballX;
if (Math.random() >= 0.5) {
    ballX = game.gameWidth / 4;
} else {
    ballX = game.gameWidth * 3 / 4;
}
game.resetPositions(ballX);

var updateRate = 500;
var dt, now, last = game.timestamp(), step = 1 / updateRate;

function frame() {
    now = game.timestamp();
    dt = Math.min(1, (now - last) / 1000);

    while(dt > step) {
        dt = dt - step;
        game.update(step);
    }

    game.draw();
    last = now - (dt % step);
    requestAnimationFrame(frame);
}

requestAnimationFrame(frame);