export default class AI {
    constructor(game) {
        this.game = game;
        game.p1.ai = this;
        game.p2.ai = this;
    }

    // return an action based on the state of the game
    getAction(x, margin) {
        var action, mult, xLand = this.predictBallLandingPosition();
        // pl
        if (x < this.game.gameWidth / 2) {
            // ball will land on p1 side
            if (xLand < this.game.gameWidth / 2) {
                // go to just behind ball landing spot
                if (x > this.game.gameWidth * 3 / 8) {
                    mult = 1 / 4;
                } else if (x > this.game.gameWidth * 4 / 8) {
                    mult = 1 / 2;
                } else {
                    mult = 3 / 4;
                }
                if (x < xLand - this.game.p1.radius * 3 / 4) {
                    action = "right";
                } else {
                    action = "left";
                }
                if (Math.abs(x - (xLand - this.game.p1.radius * 3 / 4)) < margin) {
                    action = "stop";
                }
            // ball will land on p2 side
            } else {
                // go to center of p1 side
                if (x < this.game.gameWidth / 4) {
                    action = "right";
                } else {
                    action = "left";
                }
                if (Math.abs(x - (this.game.gameWidth / 4)) < margin) {
                    action = "stop";
                }
            }
        // p2
        } else {
            // ball will land on p2 side
            if (xLand > this.game.gameWidth / 2) {
                // go to just behind ball landing spot
                if (x < this.game.gameWidth * 5 / 8) {
                    mult = 1 / 4;
                } else if (x < this.game.gameWidth * 6 / 8) {
                    mult = 1 / 2;
                } else {
                    mult = 3 / 4;
                }
                if (x < xLand + this.game.p2.radius * mult) {
                    action = "right";
                } else {
                    action = "left";
                }
                if (Math.abs(x - (xLand + this.game.p2.radius * mult)) < margin) {
                    action = "stop";
                }
                if (xLand < this.game.gameWidth / 2 + this.game.p2.radius * 2.5 &&
                    Math.abs(x - (xLand + this.game.p2.radius * mult)) < margin &&
                    this.game.ball.y > this.game.gameHeight - this.game.p2.radius * 2.5 &&
                    this.game.ball.yv > 0) {
                        action = "jump";
                }
            // ball will land on p1 side
            } else {
                // go to center of p2 side
                if (x < this.game.gameWidth * 3 / 4) {
                    action = "right";
                } else {
                    action = "left";
                }
                if (Math.abs(x - (this.game.gameWidth * 3 / 4)) < margin) {
                    action = "stop";
                }
            }
        }
        return action;
    }
    
    // predict the horizontal position of the ball when it contacts the floor
    predictBallLandingPosition() {
        var     r = this.game.ball.radius,
                x = this.game.ball.x,
                y = this.game.ball.y,
                xv = this.game.ball.xv,
                yv = this.game.ball.yv,
                g = this.game.gravity,
                gameWidth = this.game.gameWidth,
                gameHeight = this.game.gameHeight;
        
        // frames: number of frames elapsed during ball's flight
        var frames1 = (-yv + Math.sqrt((Math.pow(yv, 2) - 2 * g * (y - gameHeight + r)))) / g;
        var frames2 = (-yv - Math.sqrt((Math.pow(yv, 2) - 2 * g * (y - gameHeight + r)))) / g;
        var frames = Math.max(frames1, frames2);

        // d: total horizontal distance traveled by ball during flight (pixels), disregarding walls
		var d = xv * frames;

		// x_intercept: final x-position of ball when it lands, disregarding walls
        var x_intercept = x + d;
        
        // ball will not hit a wall
        var x_final;
        if (x_intercept + r < gameWidth && x_intercept - r > 0) {
            x_final = x_intercept;
        // ball will hit at least one wall
        } else {
            if (xv > 0) {
                x_final = gameWidth - (x_intercept - gameWidth) - 2 * r;
            } else {
                x_final = 2 * r - x_intercept;
            }
        }

        return x_final;
    }
}