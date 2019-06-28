import InputHandler from "/src/input.js";

export default class Player {
    constructor(name, radius, speed, accel, jump, inputs, color, isAI) {
        this.name = name;
        this.radius = radius;
        this.speed = speed;
        this.accel = accel;
        this.jump = jump;
        this.inputs = inputs;
        this.color = color;
        this.isAI = isAI;

        this.x = 150;
        this.y = 300;
        this.xv = 0;
        this.yv = 0;
        this.jumpHeldDown = false;
        this.jumpEnabled = true;

        this.inputHandler = new InputHandler(this);
    }

    getPupilOffet(ball, eyeXOffset, eyeYOffset, pupilOffsetRatio) {
        let xDiff = -(ball.x - (this.x + eyeXOffset));
        let yDiff = -(ball.y - (this.y - eyeYOffset));
        let atanDegrees = this.degrees(Math.atan(yDiff / xDiff));
        let angle = 0, xShift = 0, yShift = 0;
        if (xDiff > 0) {
            angle = atanDegrees;
            xShift = -pupilOffsetRatio * Math.cos(this.radians(angle));
            yShift = -pupilOffsetRatio * Math.sin(this.radians(angle));
        } else if (xDiff < 0) {
            if (yDiff > 0) {
                angle = 180 + atanDegrees;
            } else if (yDiff < 0) {
                angle = -180 + atanDegrees;
            }
            xShift = -pupilOffsetRatio * Math.cos(this.radians(angle));
            yShift = -pupilOffsetRatio * Math.sin(this.radians(angle));
        } else if (xDiff == 0) {
            if (yDiff > 0) {
                angle = -90;
            } else {
                angle = 90
            }
            xShift = pupilOffsetRatio * Math.cos(this.radians(angle));
            yShift = pupilOffsetRatio * Math.sin(this.radians(angle));
        } else if (yDiff == 0) {
            angle = 180;
            xShift = pupilOffsetRatio * Math.cos(this.radians(angle));
            yShift = pupilOffsetRatio * Math.sin(this.radians(angle));
        }
        return [xShift, yShift];
    }

    degrees(radians) {
        return (radians * 180) / Math.PI;
    }

    radians(degrees) {
        return (degrees * Math.PI) / 180;
    }

    update(gravity, gameHeight, deltaTime) {
        if (this.y < gameHeight) {
            this.yv += gravity;
        }
        
        this.x += this.xv / deltaTime;
        this.y += this.yv / deltaTime;
    }

    draw(ctx, gameWidth, gameHeight, ball) {
        // body
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI, true);
        ctx.fill();
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#003300";
        ctx.stroke();

        // underline
        ctx.fillStyle = "#000000";
        ctx.moveTo(this.x - this.radius, this.y);
        ctx.lineTo(this.x + this.radius, this.y);
        ctx.stroke();

        // eye & pupil
        let eyeXOffset = this.radius / 2;
        let eyeYOffset = this.radius * 3 / 5;
        let eyeRadius = this.radius / 4;
        let pupilRadius = this.radius / 8;
        let pupilOffsetRatio = this.radius / 10;
        let pupilOffsetX = 0, pupilOffsetY = 0;

        if (ball.y + ball.radius >= gameHeight - 10) {
            if ((this.x < gameWidth / 2 && ball.x < gameWidth / 2) || (this.x > gameWidth / 2 && ball.x > gameWidth / 2)) {
                eyeRadius = this.radius / 3;
            }
        }

        if (this.x > gameWidth / 2) {
            eyeXOffset = -eyeXOffset;
        }

        ctx.fillStyle = "#D3D3D3";
        ctx.beginPath();
        ctx.arc(this.x + eyeXOffset, this.y - eyeYOffset, eyeRadius, 0, 2 * Math.PI, false);
        ctx.fill();
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#000000";
        ctx.stroke();

        [pupilOffsetX, pupilOffsetY] = this.getPupilOffet(ball, eyeXOffset, eyeYOffset, pupilOffsetRatio);
        ctx.fillStyle = "#000000";
        ctx.beginPath();
        ctx.arc(this.x + eyeXOffset + pupilOffsetX, this.y - eyeYOffset + pupilOffsetY, pupilRadius, 0, 2 * Math.PI, false);
        ctx.fill();
        ctx.lineWidth = 1;
        ctx.strokeStyle = "#000000";
        ctx.stroke();
    }
}