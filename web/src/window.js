export default class WindowHandler{
    constructor(canvas, game, pct) {
        this.canvas = canvas;
        this.game = game;
        this.pct = pct;
    
        function resizeCanvas() {
            if (window.innerHeight * pct * 2 > window.innerWidth * pct) {
                return [window.innerWidth * pct, window.innerWidth * pct / 2];
            } else {
                return [window.innerHeight * pct * 2, window.innerHeight * pct];
            }
        }

        window.addEventListener("resize", function() {
            [canvas.width, canvas.height] = resizeCanvas();
            game.resize(canvas.width, canvas.height);
        });
    }

    resizeGameWindow() {
        [this.canvas.width, this.canvas.height] = this.resizeCanvas();
        this.game.resize(this.canvas.width, this.canvas.height);
    }

    resizeCanvas() {
        if (window.innerHeight * this.pct * 2 > window.innerWidth * this.pct) {
            return [window.innerWidth * this.pct, window.innerWidth * this.pct / 2];
        } else {
            return [window.innerHeight * this.pct * 2, window.innerHeight * this.pct];
        }
    }
}