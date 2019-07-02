export default class InputHandler{
    constructor(player) {
        let left = player.inputs.left;
        let right = player.inputs.right;
        let jump = player.inputs.jump;
        let slow = player.inputs.slow;
        let toggleAI = player.inputs.toggleAI;

        document.addEventListener("keydown", (event) => {
            switch(event.keyCode) {
                case left:
                    player.keyAction("left", null);
                    break;
                case right:
                    player.keyAction("right", null);
                    break;
                case jump:
                    player.keyAction("jump", null);
                    break;
                case slow:
                    player.keyAction("slow", null);
                    break;
                case toggleAI:
                    player.isAI = !player.isAI;
                    break;
            }
        });

        document.addEventListener("keyup", (event) => {
            switch(event.keyCode) {
                case left:
                    player.keyAction(null, "left");
                    break;
                case right:
                    player.keyAction(null, "right");
                    break;
                case jump:
                    player.keyAction(null, "jump");
                    break;
                case slow:
                    player.keyAction(null, "slow");
                    break;
            }
        });
    }
}