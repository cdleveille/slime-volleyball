export default class Game {
    constructor(gameWidth, gameHeight, ball, gravity, bounce) {
        this.gameWidth = gameWidth;
        this.gameHeight = gameHeight;
        this.ball = ball;
        this.gravity = gravity;
        this.bounce = bounce;
    }

    handleCollisions() {
        // Ball contacts floor
        if (this.ball.y > this.gameHeight - this.ball.radius) {
            this.ball.yv = -this.ball.yv * this.bounce;
        }

        // Ball contacts wall
        if (this.ball.x < this.ball.radius || this.ball.x > this.gameWidth - this.ball.radius) {
            this.ball.xv = -this.ball.xv * this.bounce;
        }
    }

    update() {
        this.ball.update(this.gravity);
    }

    draw(ctx) {
        this.ball.draw(ctx);
    }


}