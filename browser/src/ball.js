export default class Ball {
    constructor(radius) {
        this.x = 200;
        this.y = 100;
        this.xv = 5;
        this.yv = 0;
        this.maxV = 15;
        this.radius = radius;
        //this.color = color;
    }

    update(gravity) {
        this.yv += gravity;

        //TODO: enforce max speed

        this.x += this.xv;
        this.y += this.yv;
    }

    draw(ctx) {
        ctx.fillStyle = 'green';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
        ctx.fill();
        ctx.lineWidth = 1;
        ctx.strokeStyle = '#003300';
        ctx.stroke();
    }

    drawXInd(ctx) {
        //TODO: if the ball is off-screen, draw a marker indicating its horizontal location
    }
}