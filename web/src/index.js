// http-server -a localhost -p 8000 -c-1    http://localhost:8000/index.html

import Ball from "/src/ball.js";
import Player from "/src/player.js";
import Game from "/src/game.js";
import WindowHandler from "/src/window.js";
import AI from "/src/ai.js";

let canvas = document.getElementById("gameScreen");
let ctx = canvas.getContext("2d");

let scoreLimit = 10,
    windowPercent = 0.95,
    ballRadiusMult = 1.00,
    playerRadiusMult = 1.0,
    playerSpeedMult = 1.00,
    playerJumpMult = 1.00,
    netWidthMult = 1.00,
    netHeightMult = 1.00,
    gravityMult = 1.00,
    bounce = 0.97,
    bounceNet = 0.80,
    momentumTransfer = 0.15;

let p1Inputs = { left: 65, right: 68, jump: 87 , slow: 83, toggleAI: 49 };
let p2Inputs = { left: 37, right: 39, jump: 38 , slow: 40, toggleAI: 50 };

let p1 = new Player(playerRadiusMult, playerSpeedMult, playerJumpMult, p1Inputs, "#00008B", false);
let p2 = new Player(playerRadiusMult, playerSpeedMult, playerJumpMult, p2Inputs, "#8B0000", true);

let ball = new Ball(ballRadiusMult, '#006400');

let game = new Game(scoreLimit, ctx, "#ADD8E6", p1, p2, ball, netWidthMult, netHeightMult, 
                    "#000000", gravityMult, bounce, bounceNet, momentumTransfer);

let ai = new AI(game);

let wh = new WindowHandler(canvas, game, windowPercent);
wh.resizeGameWindow();

let ballX;
if (Math.random() >= 0.5) {
    ballX = game.gameWidth / 4;
} else {
    ballX = game.gameWidth * 3 / 4;
}
game.resetPositions(ballX);

let updateRate = 500;
let dt, now, last = game.timestamp(), step = 1 / updateRate;

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