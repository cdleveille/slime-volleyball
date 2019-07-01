export default class WindowHandler{
    constructor(canvas, game) {
        this.canvas = canvas;
        this.game = game;
    
        function resizeCanvas() {
            if ((window.innerHeight * 0.95) * 2 > window.innerWidth * 0.95) {
                return [window.innerWidth * 0.95, window.innerWidth * 0.475];
            } else {
                return [window.innerHeight * 1.9, window.innerHeight * 0.95];
            }
        }

        window.addEventListener("resize", function() {
            [canvas.width, canvas.height] = resizeCanvas();
            game.resize(canvas.width, canvas.height);
        }, true);
    }

    resizeGameWindow() {
        [this.canvas.width, this.canvas.height] = this.resizeCanvas();
        this.game.resize(this.canvas.width, this.canvas.height);
    }

    resizeCanvas() {
        if ((window.innerHeight * 0.95) * 2 > window.innerWidth * 0.95) {
            return [window.innerWidth * 0.95, window.innerWidth * 0.475];
        } else {
            return [window.innerHeight * 1.9, window.innerHeight * 0.95];
        }
    }
}