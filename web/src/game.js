export default class Game {
    constructor(scoreLimit, ctx, gameWidth, gameHeight, backgroundColor, p1, p2, ball, netWidth, netHeight, netColor, gravity, bounce, bounceNet) {
        this.scoreLimit = scoreLimit;
        this.ctx = ctx;
        this.gameWidth = gameWidth;
        this.gameHeight = gameHeight;
        this.backgroundColor = backgroundColor;
        this.p1 = p1;
        this.p2 = p2;
        this.p1Score = 0;
        this.p2Score = 0;
        this.players = [p1, p2];
        this.ball = ball;
        this.netWidth = netWidth;
        this.netHeight = netHeight;
        this.netColor = netColor;
        this.gravity = gravity;
        this.bounce = bounce;
        this.bounceNet = bounceNet;
        this.gameOver = false;
        this.isFrozen = false;
        this.frozenAtTime;
    }

    resetPositions(ballX) {
        this.ball.x = ballX;
        this.ball.y = this.gameHeight / 3;
        this.ball.xv = 0;
        this.ball.yv = 0;

        this.p1.x = this.gameWidth / 4;
        this.p1.y = this.gameHeight;
        this.p1.jumpEnabled = true;

        this.p2.x = this.gameWidth * 3 / 4;
        this.p2.y = this.gameHeight;
        this.p2.jumpEnabled = true;
    }

    handleCollisions() {
        // p1 contacts floor
        if (this.p1.y >= this.gameHeight) {
            this.p1.y = this.gameHeight;
            this.p1.jumpEnabled = true;
            if (this.p1.jumpHeldDown) {
                this.p1.yv = -this.p1.jump;
                this.p1.jumpEnabled = false;
            }
        }

        // p2 contacts floor
        if (this.p2.y >= this.gameHeight) {
            this.p2.y = this.gameHeight;
            this.p2.jumpEnabled = true;
            if (this.p2.jumpHeldDown) {
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

        // ball contacts floor
        if (this.ball.y >= this.gameHeight - this.ball.radius) {
            this.ball.y = this.gameHeight - this.ball.radius

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

        // ball contacts wall
        if (this.ball.x < this.ball.radius) {
            this.ball.x = this.ball.radius;
            this.ball.xv = -this.ball.xv * this.bounce;
        } else if (this.ball.x > this.gameWidth - this.ball.radius) {
            this.ball.x = this.gameWidth - this.ball.radius;
            this.ball.xv = -this.ball.xv * this.bounce;
        }

        // ball contacts net
        if (this.ballContactsCircle(this.gameWidth / 2, this.gameHeight - this.netHeight + (this.netWidth / 2), this.netWidth / 2)) {
            [this.ball.x, this.ball.y] = this.getBallContactsCirclePosition(this.gameWidth / 2, this.gameHeight - this.netHeight + (this.netWidth / 2), this.netWidth / 2);
            [this.ball.xv, this.ball.yv] = this.getBallContactsCircleVelocity(this.gameWidth / 2, this.gameHeight - this.netHeight + (this.netWidth / 2), 0, 0, this.bounceNet);
        } else if (this.ball.y > this.gameHeight - this.netHeight + this.netWidth) {
            if (Math.abs(this.gameWidth / 2 - (this.ball.x + this.ball.radius)) <= this.netWidth / 2) {
                this.ball.x = this.gameWidth / 2 - this.netWidth / 2 - this.ball.radius;
                this.ball.xv = -this.ball.xv * this.bounceNet;
            } else if (Math.abs((this.ball.x - this.ball.radius) - this.gameWidth / 2) <= this.netWidth / 2) {
                this.ball.x = this.gameWidth / 2 + this.netWidth / 2 + this.ball.radius;
                this.ball.xv = -this.ball.xv * this.bounceNet;
            }
        }

        // ball contacts player
        for (let i = 0; i < this.players.length; i++) {
            let player = this.players[i];
            if (this.ballContactsCircle(player.x, player.y, player.radius)) {
                [this.ball.x, this.ball.y] = this.getBallContactsCirclePosition(player.x, player.y, player.radius);
                [this.ball.xv, this.ball.yv] = this.getBallContactsCircleVelocity(player.x, player.y, player.xv, player.yv, this.bounce);
            }
        }
    }

    ballContactsCircle(x, y, r) {
        if (Math.sqrt( Math.pow(this.ball.x - x, 2) + Math.pow(this.ball.y - y, 2) ) <= this.ball.radius + r) {
            return true
        }
		return false
    }

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

    getBallContactsCircleVelocity(x, y, xv, yv, bounce) {
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
        xvFinal = (xSpeed + (xv * 0.12)) * bounce * 1.03;
        yvFinal = (ySpeed + (yv * 0.12)) * bounce * 1.03;
        return [xvFinal, yvFinal];
    }

    degrees(radians) {
        return (radians * 180) / Math.PI;
    }

    radians(degrees) {
        return (degrees * Math.PI) / 180;
    }

    freeze(ms) {
        var now = new Date().getTime();
        while (new Date().getTime() < now + ms) {}
    }

    timestamp() {
        return window.performance && window.performance.now ? window.performance.now() : new Date().getTime();
    }

    update(deltaTime) {
        if (!this.isFrozen) {
            deltaTime = deltaTime * 200;
            this.ball.update(this.gravity, deltaTime);
            this.p1.update(this.gravity, this.gameHeight, deltaTime);
            this.p2.update(this.gravity, this.gameHeight, deltaTime);
        }
        this.handleCollisions();
    }

    draw() {
        this.ctx.clearRect(0, 0, this.gameWidth, this.gameHeight);

        this.ctx.fillStyle = this.backgroundColor;
        this.ctx.fillRect(0, 0, this.gameWidth, this.gameHeight);

        this.ctx.fillStyle = "#000000";
        this.ctx.font = "42px Arial";
        this.ctx.fillText(this.p1Score, 30, 50);
        this.ctx.fillText(this.p2Score, this.gameWidth - 65, 50);

        if (this.gameOver) {
            this.ctx.fillStyle = "#000000";
            this.ctx.font = "42px Arial";
            this.ctx.fillText("Game Over!", this.gameWidth / 2 - 120, 50);
        }

        this.ctx.fillStyle = this.netColor;
        this.ctx.fillRect(this.gameWidth / 2 - this.netWidth / 2, this.gameHeight - this.netHeight + this.netWidth / 2, this.netWidth, this.netHeight);
        this.ctx.beginPath();
        this.ctx.arc(this.gameWidth / 2, this.gameHeight - this.netHeight + this.netWidth / 2, this.netWidth / 2, 0, 2 * Math.PI, false);
        this.ctx.fill();

        this.p1.draw(this.ctx, this.gameWidth, this.gameHeight, this.ball);
        this.p2.draw(this.ctx, this.gameWidth, this.gameHeight, this.ball);

        this.ball.draw(this.ctx);
    }
}