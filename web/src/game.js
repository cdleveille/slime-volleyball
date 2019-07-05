export default class Game {
    constructor(scoreLimit, ctx, backgroundColor, p1, p2, ball, netWidthMult, netHeightMult, netColor, gravityMult, bounce, bounceNet, momentumTransfer) {
        this.scoreLimit = scoreLimit;
        this.ctx = ctx;
        this.gameWidth = window.innerWidth
        this.gameHeight = window.innerHeight;
        this.backgroundColor = backgroundColor;
        this.p1 = p1;
        this.p2 = p2;
        this.players = [p1, p2];
        this.p1.game = this;
        this.p2.game = this;
        this.p1Score = 0;
        this.p2Score = 0;
        this.ball = ball;
        this.ball.game = this;
        this.netWidthMult = netWidthMult;
        this.netHeightMult = netHeightMult;
        this.netColor = netColor;
        this.gravityMult = gravityMult;
        this.bounce = bounce;
        this.bounceNet = bounceNet;
        this.momentumTransfer = momentumTransfer;
        this.gameOver = false;
    }

    // initialize the position of the game objects at the start of a new point
    resetPositions(ballX) {
        this.ball.x = ballX;
        this.ball.y = this.gameHeight / 3;
        this.ball.xv = 0;
        this.ball.yv = 0;

        this.p1.x = this.gameWidth / 4;
        this.p1.y = this.gameHeight;
        this.p1.xv = 0;
        this.p1.yv = 0;
        this.p1.jumpEnabled = true;

        this.p2.x = this.gameWidth * 3 / 4;
        this.p2.y = this.gameHeight;
        this.p2.xv = 0;
        this.p2.yv = 0;
        this.p2.jumpEnabled = true;

        this.isFrozen = false;
    }

    // detect and account for various game object collision events
    handleCollisions() {
        // p1 contacts floor
        if (this.p1.y >= this.gameHeight) {
            this.p1.y = this.gameHeight;
            this.p1.jumpEnabled = true;
            if (this.p1.jumpHeldDown && !this.p1.isAI) {
                this.p1.yv = -this.p1.jump;
                this.p1.jumpEnabled = false;
            }
        }

        // p2 contacts floor
        if (this.p2.y >= this.gameHeight) {
            this.p2.y = this.gameHeight;
            this.p2.jumpEnabled = true;
            if (this.p2.jumpHeldDown && !this.p2.isAI) {
                this.p2.yv = -this.p2.jump;
                this.p2.jumpEnabled = false;
            }
        }

        // keep p1 inbounds
        if (this.p1.x < this.p1.radius) {
            this.p1.x = this.p1.radius;
        } else if (this.p1.x > this.gameWidth / 2 - this.netWidth / 2 - this.p1.radius) {
            this.p1.x = this.gameWidth / 2 - this.netWidth / 2 - this.p1.radius;
        }

        // keep p2 inbounds
        if (this.p2.x < this.gameWidth / 2 + this.netWidth / 2 + this.p2.radius) {
            this.p2.x = this.gameWidth / 2 + this.netWidth / 2 + this.p2.radius;
        } else if (this.p2.x > this.gameWidth - this.p2.radius) {
            this.p2.x = this.gameWidth - this.p2.radius;
        }

        // ball contacts player
        for (let i = 0; i < this.players.length; i++) {
            let player = this.players[i];
            if (this.ballContactsCircle(player.x, player.y, player.radius)) {
                [this.ball.x, this.ball.y] = this.getBallContactsCirclePosition(player.x, player.y, player.radius);
                [this.ball.xv, this.ball.yv] = this.getBallContactsCircleVelocity(player.x, player.y, player.xv, player.yv, 1, this.momentumTransfer);
            }
        }

        // ball contacts net
        if (this.ballContactsNetTop()) {
            [this.ball.x, this.ball.y] = this.getBallContactsCirclePosition(this.gameWidth / 2, this.gameHeight - this.netHeight + (this.netWidth / 2), this.netWidth / 2);
            [this.ball.xv, this.ball.yv] = this.getBallContactsCircleVelocity(this.gameWidth / 2, this.gameHeight - this.netHeight + (this.netWidth / 2), 0, 0, this.bounceNet, 0);
        } else if (this.ballContactsNetBottomLeft()) {
            this.ball.x = this.gameWidth / 2 - this.netWidth / 2 - this.ball.radius;
            this.ball.y += this.ball.yv;
            this.ball.xv = -this.ball.xv * this.bounceNet;
        } else if (this.ballContactsNetBottomRight()) {
            this.ball.x = this.gameWidth / 2 + this.netWidth / 2 + this.ball.radius;
            this.ball.y += this.ball.yv;
            this.ball.xv = -this.ball.xv * this.bounceNet;
        }

        // ball contacts wall
        if (this.ball.x < this.ball.radius) {
            this.ball.x = this.ball.radius;
            this.ball.y += this.ball.yv;
            this.ball.xv = -this.ball.xv * this.bounce;
        } else if (this.ball.x > this.gameWidth - this.ball.radius) {
            this.ball.x = this.gameWidth - this.ball.radius;
            this.ball.y += this.ball.yv;
            this.ball.xv = -this.ball.xv * this.bounce;
        }

        // ball contacts floor
        if (this.ball.y >= this.gameHeight - this.ball.radius) {
            this.ball.y = this.gameHeight - this.ball.radius
            this.ball.yv = -this.ball.yv * this.bounce;

            if (!this.isFrozen) {
                this.isFrozen = true;
                this.frozenAtTime = this.timestamp();
                
                if (!this.gameOver) {
                    if (this.ball.x < this.gameWidth / 2) {
                        this.p2Score++;
                    } else {
                        this.p1Score++;
                    }
                }
                if (this.p1Score == this.scoreLimit || this.p2Score == this.scoreLimit) {
                    this.gameOver = true;
                }
            } else if (this.timestamp() - this.frozenAtTime >= 500) {
                this.isFrozen = false;
                var ballX;
                if (this.ball.x < this.gameWidth / 2) {
                    ballX = this.gameWidth * 3 / 4;
                    
                } else {
                    ballX = this.gameWidth / 4;
                }
                this.resetPositions(ballX);
            }
        }
    }

    // determine whether the ball is contacting the given circular object
    ballContactsCircle(x, y, r) {
        if (Math.sqrt( Math.pow(this.ball.x - x, 2) + Math.pow(this.ball.y - y, 2) ) <= this.ball.radius + r) {
            return true
        }
		return false
    }

    // determine whether the ball is contacting the top of the net
    ballContactsNetTop() {
        return this.ballContactsCircle(this.gameWidth / 2, this.gameHeight - this.netHeight + (this.netWidth / 2), this.netWidth / 2);
    }

    // determine whether the ball is contacting the left side of the bottom of the net
    ballContactsNetBottomLeft() {
        return this.ball.y > this.gameHeight - this.netHeight + this.netWidth &&
            Math.abs(this.ball.x + this.ball.radius - this.gameWidth / 2) < this.netWidth / 2 &&
            this.ball.xv > 0;
    }

    // determine whether the ball is contacting the right side of the bottom of the net
    ballContactsNetBottomRight() {
        return this.ball.y > this.gameHeight - this.netHeight + this.netWidth && 
            Math.abs(this.ball.x - this.ball.radius - this.gameWidth / 2) < this.netWidth / 2 &&
            this.ball.xv < 0;
    }

    // calculate the position of the ball tangent to the arc of the circular object it has contacted
    getBallContactsCirclePosition(x, y, r) {
        let combinedRadius = this.ball.radius + r;
        let xDiff = -(this.ball.x - x);
        let yDiff = -(this.ball.y - y);
        let atanDegrees = this.degrees(Math.atan(yDiff / xDiff));
        let angle = 0, xShift = 0, yShift = 0, xvFinal = 0, yvFinal = 0;
        if (xDiff > 0) {
            angle = atanDegrees;
            xShift = -combinedRadius * Math.cos(this.radians(angle));
            yShift = -combinedRadius * Math.sin(this.radians(angle));
        } else if (xDiff < 0) {
            if (yDiff > 0) {
                angle = 180 + atanDegrees;
            } else if (yDiff < 0) {
                angle = -180 + atanDegrees;
            }
            xShift = -combinedRadius * Math.cos(this.radians(angle));
            yShift = -combinedRadius * Math.sin(this.radians(angle));
        } else if (xDiff == 0) {
            if (yDiff > 0) {
                angle = -90;
            } else {
                angle = 90
            }
            xShift = combinedRadius * Math.cos(this.radians(angle));
            yShift = combinedRadius * Math.sin(this.radians(angle));
        } else if (yDiff == 0) {
            angle = 180;
            xShift = combinedRadius * Math.cos(this.radians(angle));
            yShift = combinedRadius * Math.sin(this.radians(angle));
        }
        return [x + xShift, y + yShift];
    }

    // calculate the rebound velocity vector of the ball when it bounces off of a circular object
    getBallContactsCircleVelocity(x, y, xv, yv, bounce, momentumTransfer) {
        let ballSpeed = Math.sqrt( Math.pow(this.ball.xv, 2) + Math.pow(this.ball.yv, 2) );
        let xDiff = -(this.ball.x - x);
        let yDiff = -(this.ball.y - y);
        let atanDegrees = this.degrees(Math.atan(yDiff / xDiff));
        let angle = 0, xSpeed = 0, ySpeed = 0, xvFinal = 0, yvFinal = 0;
        if (xDiff > 0) {
            angle = atanDegrees;
            xSpeed = -ballSpeed * Math.cos(this.radians(angle));
            ySpeed = -ballSpeed * Math.sin(this.radians(angle));
        } else if (xDiff < 0) {
            if (yDiff > 0) {
                angle = 180 + atanDegrees;
            } else if (yDiff < 0) {
                angle = -180 + atanDegrees;
            }
            xSpeed = -ballSpeed * Math.cos(this.radians(angle));
            ySpeed = -ballSpeed * Math.sin(this.radians(angle));
        } else if (xDiff == 0) {
            if (yDiff > 0) {
                angle = -90;
            } else {
                angle = 90
            }
            xSpeed = ballSpeed * Math.cos(this.radians(angle));
            ySpeed = ballSpeed * Math.sin(this.radians(angle));
        } else if (yDiff == 0) {
            angle = 180;
            xSpeed = ballSpeed * Math.cos(this.radians(angle));
            ySpeed = ballSpeed * Math.sin(this.radians(angle));
        }
        xvFinal = (xSpeed + (xv * momentumTransfer)) * bounce;
        yvFinal = (ySpeed + (yv * momentumTransfer)) * bounce;
        return [xvFinal, yvFinal];
    }

    // convert radians to degrees
    degrees(radians) {
        return (radians * 180) / Math.PI;
    }

    // convert degrees to radians
    radians(degrees) {
        return (degrees * Math.PI) / 180;
    }

    // get the current time with high precision
    timestamp() {
        return window.performance && window.performance.now ? window.performance.now() : new Date().getTime();
    }

    // adapt all scalable game fields to the size of the window
    resize(newWidth, newHeight) {

        this.ball.x = newWidth * (this.ball.x / this.gameWidth);
        this.ball.y = newHeight * (this.ball.y / this.gameHeight);
        this.ball.xv = this.ball.xv * (newWidth / this.gameWidth);
        this.ball.yv = this.ball.yv * (newHeight / this.gameHeight);
        this.ball.radius = newWidth * (24 / 1200) * this.ball.radiusMult;

        this.p1.x = newWidth * (this.p1.x / this.gameWidth);
        this.p1.y = newHeight * (this.p1.y / this.gameHeight);
        this.p1.xv = this.p1.xv * (newWidth / this.gameWidth);
        this.p1.yv = this.p1.yv * (newHeight / this.gameHeight);
        this.p1.radius = newWidth * (56 / 1200) * this.p1.radiusMult;
        this.p1.speed = newWidth * (5 / 1200) * this.p1.speedMult;
        this.p1.jump = newWidth * (5 / 1200) * this.p1.jumpMult;

        this.p2.x = newWidth * (this.p2.x / this.gameWidth);
        this.p2.y = newHeight * (this.p2.y / this.gameHeight);
        this.p2.xv = this.p2.xv * (newWidth / this.gameWidth);
        this.p2.yv = this.p2.yv * (newHeight / this.gameHeight);
        this.p2.radius = newWidth * (56 / 1200) * this.p2.radiusMult;
        this.p2.speed = newWidth * (5 / 1200) * this.p2.speedMult;
        this.p2.jump = newWidth * (5 / 1200) * this.p2.jumpMult;

        this.gravity = newWidth * (0.1 / 1200) * this.gravityMult;
        this.netWidth = newWidth * (20 / 1200) * this.netWidthMult;
        this.netHeight = newWidth * (100 / 1200) * this.netHeightMult;
        this.gameWidth = newWidth;
        this.gameHeight = newHeight;
        this.isFrozen = false;
    }

    // update the position/velocity of game objects
    update(step) {
        if (!this.isFrozen) {
            step = step * 170;
            this.p1.update(step);
            this.p2.update(step);
            this.ball.update(step);
        }
        this.handleCollisions();
    }

    // render the current state of the game
    draw() {
        // clear and fill with background color
        this.ctx.clearRect(0, 0, this.gameWidth, this.gameHeight);
        this.ctx.fillStyle = this.backgroundColor;
        this.ctx.fillRect(0, 0, this.gameWidth, this.gameHeight);

        // set game font size based on dimensions of game
        if (this.gameWidth > 1000) {
            this.ctx.font = "42px Arial";
        } else if (this.gameWidth > 900){
            this.ctx.font = "39px Arial";
        } else if (this.gameWidth > 800){
            this.ctx.font = "34px Arial";
        } else if (this.gameWidth > 700){
            this.ctx.font = "29px Arial";
        } else if (this.gameWidth > 600){
            this.ctx.font = "25px Arial";
        } else if (this.gameWidth > 500){
            this.ctx.font = "21px Arial";
        } else if (this.gameWidth > 400){
            this.ctx.font = "17px Arial";
        } else if (this.gameWidth > 300){
            this.ctx.font = "13px Arial";
        } else if (this.gameWidth > 200){
            this.ctx.font = "8px Arial";
        } else if (this.gameWidth > 100){
            this.ctx.font = "4px Arial";
        } else {
            this.ctx.font = "2px Arial";
        }

        // draw player scores
        this.ctx.fillStyle = "#000000";
        this.ctx.fillText(this.p1Score, this.gameWidth / 40, this.gameHeight / 12);
        this.ctx.fillText(this.p2Score, this.gameWidth * 0.95, this.gameHeight / 12);

        // draw game over message if applicable
        if (this.gameOver) {
            this.ctx.fillStyle = "#000000";
            this.ctx.fillText("Game Over!", this.gameWidth / 2 - (this.gameWidth / 10), (this.gameHeight / 12));
        }

        // draw net
        this.ctx.fillStyle = this.netColor;
        this.ctx.fillRect(this.gameWidth / 2 - this.netWidth / 2, this.gameHeight - this.netHeight + this.netWidth / 2, this.netWidth, this.netHeight);
        this.ctx.beginPath();
        this.ctx.arc(this.gameWidth / 2, this.gameHeight - this.netHeight + this.netWidth / 2, this.netWidth / 2, 0, 2 * Math.PI, false);
        this.ctx.fill();

        // draw players
        this.p1.draw();
        this.p2.draw();

        // draw ball
        this.ball.draw();
    }
}