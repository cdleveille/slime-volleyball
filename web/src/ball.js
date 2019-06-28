export default class Ball {
    constructor(radius, color) {
        this.x = 200;
        this.y = 100;
        this.xv = 3;
        this.yv = 0;
        this.maxV = 15;
        this.radius = radius;
        this.color = color;
    }

    update(gravity, deltaTime) {
        this.yv += gravity;

        // enforce max speed
        if (Math.abs(this.xv) > this.maxV) {
            this.xv = this.maxV * (this.xv / Math.abs(this.xv));
        }
        if (Math.abs(this.yv) > this.maxV) {
            this.yv = this.maxV * (this.yv / Math.abs(this.yv));
        }

        this.x += this.xv / deltaTime;
        this.y += this.yv / deltaTime;
    }

    draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
        ctx.fill();
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#003300";
        ctx.stroke();

        this.drawXInd(ctx);
    }

    drawXInd(ctx) {
        let radius = 0;
        if (this.y - this.radius < -450) {
            radius = 4;
        } else if (this.y - this.radius < -350) {
            radius = 5;
        } else if (this.y - this.radius < -250) {
            radius = 6;
        } else if (this.y - this.radius < -150) {
            radius = 7;
        } else if (this.y - this.radius < -50) {
            radius = 8;
        }

        if (radius > 0) {
            ctx.fillStyle = "#ADD8E6";
            ctx.beginPath();
            ctx.arc(this.x, 12, radius, 0, 2 * Math.PI, false);
            ctx.fill();
            ctx.lineWidth = 2;
            ctx.strokeStyle = "#003300";
            ctx.stroke();
        }
    }
}