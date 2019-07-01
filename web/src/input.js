export default class InputHandler{
    constructor(player) {
        let left = player.inputs.left;
        let right = player.inputs.right;
        let jump = player.inputs.jump;

        document.addEventListener("keydown", (event) => {
            switch(event.keyCode) {
                case left:
                    player.xv = -player.speed;
                    break;
                case right:
                    player.xv = player.speed;
                    break;
                case jump:
                    player.jumpHeldDown = true;
                    if (player.jumpEnabled) {
                        player.yv = -player.jump;
                        player.jumpEnabled = false;
                    }
                    break;
            }
        });

        document.addEventListener("keyup", (event) => {
            switch(event.keyCode) {
                case left:
                    if (player.xv < 0)
                        player.xv = 0;
                    break;
                case right:
                    if (player.xv > 0)
                        player.xv = 0;
                    break;
                case jump:
                    player.jumpHeldDown = false;
                    break;
            }
        });
    }
}