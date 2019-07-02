export default class AI {
    constructor(game) {
        this.game = game;
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
        var frames1 = Math.sqrt(-yv + (Math.pow(yv, 2) - 2 * g * (y - gameHeight + r))) / g;
        var frames2 = Math.sqrt(-yv + (Math.pow(yv, 2) - 2 * g * (y - gameHeight + r))) / g;
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