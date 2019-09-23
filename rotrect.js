class RotRect {
    constructor(pos, size, rot, col="(160, 32, 100)") {
        this.pos = pos;
        this.size = size;
        this.rot = rot;
        this.col = col;
        this.mid = false;
        this.cnr_pts = new Array(4).fill([0, 0]);
        this.mid_pts = new Array(4).fill([0, 0]);
        this.set_pts();
    }

    set_pts() {
        var rbx = cos(this.rot) * this.size[1] / 2 - sin(this.rot) * (this.size[0] / 2);
        var rby = sin(this.rot) * (this.size[1] / 2) + this.size[0] / 2 * cos(this.rot);

        var lbx = cos(this.rot) * this.size[1] / 2 + sin(this.rot) * (this.size[0] / 2);
        var lby = sin(this.rot) * (this.size[1] / 2) - this.size[0] / 2 * cos(this.rot);

        var rtx = -cos(this.rot) * this.size[1] / 2 - sin(this.rot) * (this.size[0] / 2);
        var rty = sin(this.rot) * (-this.size[1] / 2) + this.size[0] / 2 * cos(this.rot);

        var ltx = -cos(this.rot) * this.size[1] / 2 + sin(this.rot) * (this.size[0] / 2);
        var lty = sin(this.rot) * (-this.size[1] / 2) - this.size[0] / 2 * cos(this.rot);
        
        this.cnr_pts[0] = [this.pos[0] - ltx, this.pos[1] + lty];
        this.cnr_pts[1] = [this.pos[0] - rtx, this.pos[1] + rty];
        this.cnr_pts[2] = [this.pos[0] - rbx, this.pos[1] + rby];
        this.cnr_pts[3] = [this.pos[0] - lbx, this.pos[1] + lby];
    }

    set_mid_pts() {
        var vx = cos(this.rot) * this.size[1] / 2;
        var vy = sin(this.rot) * this.size[1] / 2;

        var hx = sin(this.rot) * this.size[0] / 2;
        var hy = cos(this.rot) * this.size[0] / 2;

        this.mid_pts[0] = [this.pos[0] + vx, this.pos[1] - vy]
        this.mid_pts[1] = [this.pos[0] + hx, this.pos[1] + hy];
        this.mid_pts[2] = [this.pos[0] - vx, this.pos[1] + vy];
        this.mid_pts[3] = [this.pos[0] - hx, this.pos[1] - hy];
    }

    update(pos, rot) {
        this.pos = pos;
        this.rot = rot;
        this.set_pts();
        if (this.mid) {
            this.set_mid_pts();
        }
    }

    render(display) {
        draw_polygon(display, this.col, this.cnr_pts);
    }

}

function draw_polygon(display, col, pts) {
    display.beginPath();
    display.moveTo(pts[0][0], pts[0][1]);
    for (var i = 1; i < pts.length; i++) {
        display.lineTo(pts[i][0], pts[i][1]);
    }
    display.fillStyle = "rgb" + col;
    display.fill();
}

function sin(x){
    return Math.sin(x);
}

function cos(x) {
    return Math.cos(x);
}