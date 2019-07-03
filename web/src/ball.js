export default class Ball {
    constructor(radiusMult, color) {
        this.radiusMult = radiusMult;
        this.color = color;
    }

    // update the position/velocity of the ball
    update(step) {
        this.yv += this.game.gravity * step;

        // enforce max speed
        if (Math.abs(this.xv) > this.radius / 1.6) {
            this.xv = this.maxV * (this.xv / Math.abs(this.xv));
        }
        if (Math.abs(this.yv) > this.radius / 1.6) {
            this.yv = this.maxV * (this.yv / Math.abs(this.yv));
        }

        this.x += this.xv * step;
        this.y += this.yv * step;
    }

    // render the ball
    draw() {
        var ctx = this.game.ctx;
        
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
        ctx.fill();
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#003300";
        ctx.stroke();
        
        this.drawXInd(ctx);
    }

    // render a horizontal position indicator if the ball is off-screen
    drawXInd(ctx) {
        let radius = 0;
        if (this.y - this.radius < -this.radius * 18) {
            radius = this.radius * (4 / 24);
        } else if (this.y - this.radius < -this.radius * 14) {
            radius = this.radius * (5 / 24);
        } else if (this.y - this.radius < -this.radius * 10) {
            radius = this.radius * (6 / 24);
        } else if (this.y - this.radius < -this.radius * 6) {
            radius = this.radius * (7 / 24);
        } else if (this.y - this.radius < -this.radius * 2) {
            radius = this.radius * (8 / 24);
        }

        if (radius > 0) {
            ctx.fillStyle = this.game.backgroundColor;
            ctx.beginPath();
            ctx.arc(this.x, this.radius / 2, radius, 0, 2 * Math.PI, false);
            ctx.fill();
            ctx.lineWidth = 2;
            ctx.strokeStyle = "#003300";
            ctx.stroke();
        }
    }
}