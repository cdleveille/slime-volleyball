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

        [canvas.width, canvas.height] = resizeCanvas();
        game.resize(canvas.width, canvas.height);
    }
}