class Car {
    constructor(world, inp=null) {
        this.world = world;
        this.inp = inp;
//        if (inp)
//            this.inp.car = this;
        this.pos = [60, 120];
        this.rot = 0;
        this.bw = 60; // body wid
        this.bl = 100; // body len
        var t_bw = $("#bw").val();
        this.bw = t_bw == "" ? this.bw : parseInt(t_bw);
        var t_bl = $("#bl").val();
        this.bl = t_bl == "" ? this.bl : parseInt(t_bl);
        this.axle = 60; // axle width
        this.wb = 70; // wheel base
        this.fw_ang = 0; // forward wheel ang
        this.max_fw_ang = radians(25);
        var t_fw = $("#fw").val();
        this.max_fw_ang = t_fw == "" ? this.max_fw_ang : radians(parseFloat(t_fw));
        this.sdz = radians(2); // steer deadzone
        this.st_speed = 0.02; // steer speed
        this.ws = 20; // wheel size
        this.ww = 12; // wheel width
        this.ms = 4.5; // move speed
        var t_ms = $("#ms").val();
        this.ms = t_ms == "" ? this.ms : parseFloat(t_ms);
        this.col_pts = new Array(8).fill([0, 0]);
        this.bdr = new RotRect(this.pos, [this.bw, this.bl], this.rot); // body rect
        this.bdr.mid = true;
        this.wr = new RotRect(this.pos, [this.axle, this.wb], this.rot); // wheel points rect
        this.wheels = this.init_wheels();
        this.sd = 300; // sensor max dist
        this.sa = 14; // sensor amount
        this.msa = radians(60); // max sensor ang
        var t_msa = $("#msa").val();
        this.msa = t_msa == "" ? this.msa : radians(parseFloat(t_msa));
        this.sds = 5; // sensor directions
        var t_sds = $("#sds").val();
        this.sds = t_sds == "" ? this.sds : parseInt(t_sds);
        this.so = 40; // sensor offset
        this.sensors = new Array(this.sds).fill(1);
        this.srp = new Array(this.sa * this.sds).fill([0, 0]); // sensor render points
        this.tpa = 20; // turn path amount (density)
        var t_tpa = $("#tpa").val();
        this.tpa = t_tpa == "" ? this.tpa : parseInt(t_tpa);
        this.tp = new Array(this.tpa).fill([0, 0]);
        this.tc = [0, 0];
        this.reverse = false;
    }

    update() {
        this.drive_by_sensors();
//        this.steer(this.inp.hor);
//        this.drive(this.inp.ver);
        this.wr.update(this.pos, this.rot);
        this.upd_sensors();
        for (var i = 0; i < 4; i++) {
            var w_rot = i < 2 ? (this.rot + this.fw_ang) : this.rot;
            this.wheels[i].update(this.wr.cnr_pts[i], w_rot);
        }
    }

    render(display) {
        this.bdr.render(display);
        for (const wl of this.wheels)
        wl.render(display);
        for (const rp of this.srp) {
            display.fillStyle = "rgb(32, 32, 255)";
            display.fillRect(rp[0], rp[1], 4, 4);
        }
        for (const rp of this.tp) {
            display.fillStyle = "rgb(32, 255, 32)";
            display.fillRect(rp[0], rp[1], 4, 4);
        }
    }

    init_wheels() {
        var w0 = new RotRect(this.wr.cnr_pts[0], [this.ww, this.ws], this.fw_ang + this.rot, "(255, 0, 0)");
        var w1 = new RotRect(this.wr.cnr_pts[1], [this.ww, this.ws], this.fw_ang + this.rot, "(255, 0, 0)");
        var w2 = new RotRect(this.wr.cnr_pts[2], [this.ww, this.ws], this.rot, "(64, 64, 64)");
        var w3 = new RotRect(this.wr.cnr_pts[3], [this.ww, this.ws], this.rot, "(64, 64, 64)");
        this.cbp = [(this.wr.cnr_pts[2][0] + this.wr.cnr_pts[3][0]) / 2, (this.wr.cnr_pts[2][1] + this.wr.cnr_pts[3][1]) / 2];
        this.cfp = [(this.wr.cnr_pts[0][0] + this.wr.cnr_pts[1][0]) / 2, (this.wr.cnr_pts[0][1] + this.wr.cnr_pts[1][1]) / 2];
        return [w0, w1, w2, w3];
    }

    steer(amount) {
        if (amount == 0)
            return;
        this.fw_ang -= amount * this.st_speed;
        //this.fw_ang = min(this.max_fw_ang, max(-this.max_fw_ang, this.fw_ang));
        this.fw_ang = between(this.fw_ang, -this.max_fw_ang, this.max_fw_ang)
    }

    drive(amount) {
        if (amount == 0)
            return;
        amount *= -1;
        var tmpf = [this.pos[0] + cos(this.rot) * this.wb / 2, this.pos[1] - sin(this.rot) * this.wb / 2];
        var tmpb = [this.pos[0] - cos(this.rot) * this.wb / 2, this.pos[1] + sin(this.rot) * this.wb / 2];
        tmpf[0] += cos(this.rot + this.fw_ang) * this.ms * amount;
        tmpf[1] -= sin(this.rot + this.fw_ang) * this.ms * amount;
        tmpb[0] += cos(this.rot) * this.ms * amount;
        tmpb[1] -= sin(this.rot) * this.ms * amount;
        var dx = (tmpf[0] + tmpb[0]) / 2;
        var dy = (tmpf[1] + tmpb[1]) / 2;
        var dr = atan2(tmpb[1] - tmpf[1], tmpf[0] - tmpb[0]);
        this.bdr.update([dx, dy], dr);
        this.set_col_pts();
        if (this.fw_ang != 0)
            this.trajectory(amount);
        if (this.coll() == false) {
            this.pos = [dx, dy];
            this.rot = dr;
            this.cfp = tmpf;
            this.cbp = tmpb;
        } else {
            this.bdr.update(this.pos, this.rot);
            this.set_col_pts();
            this.reverse = !this.reverse;
        }
    }

    set_col_pts() {
        for (var i = 0; i < 4; i++) {
            this.col_pts[i] = this.bdr.cnr_pts[i];
            this.col_pts[i + 4] = this.bdr.mid_pts[i];
        }
    }

    coll() {
        for (const clp of this.col_pts) {
            if (this.world.get_terrain(clp)) {
                return true;
            }
        }
        return false;
    }

    upd_sensors() {
        var ang_inc = this.msa * 2.0 / (this.sds - 1.0); // dif between each ang
        var angles = [];
        for (var i = 0; i < this.sds; i++) {
            angles.push(this.rot + (this.reverse ? Math.PI : 0.0) + this.msa - i * ang_inc);
        }
        var ang_i = -1;
        this.sensors.fill(1);
        for (const ang of angles) {
            ang_i += 1;
            for (var i = 0; i < this.sa; i++) {
                var cd = this.sd / this.sa * i;
                var spx = this.pos[0] + this.so * cos(ang) + cos(ang) * cd;
                var spy = this.pos[1] - this.so * sin(ang) - sin(ang) * cd;
                var sensor_point = [int(spx), int(spy)];
                this.srp[ang_i * this.sa + i] = sensor_point;
                if (this.world.get_terrain(sensor_point)) {
                    this.sensors[ang_i] = float(cd) / this.sd;
                    break;
                }
            }
        }
    }

    drive_by_sensors() {
        var pref_turn = 0;
        var mid = int(this.sds / 2);
        for (var i = 0; i < this.sds; i++) {
            if (i ==  mid)
                continue;
            pref_turn += this.sensors[i] * (i < mid ? 1.0 : -1.0);
        }
        var drive_power = this.sensors[mid] * -1.0;
        if (this.sensors[mid] <  (this.reverse ? 0.4 : 0.2))
            this.reverse = !this.reverse;
        this.drive(drive_power * (!this.reverse ? 1.0 : -1.0));
        this.steer_to(pref_turn * (!this.reverse ? 1.0 : -1.0));
    }

    steer_to(pos) {
        var pos1 = between(pos * 1.5, -1.0, 1.0);
        var pos_ang = pos1 * this.max_fw_ang;
        var dif = this.fw_ang - pos_ang;
        this.steer(signof(dif));
    }

    trajectory(speed) {
        var r = this.wb / tan(this.fw_ang);
        var cx = this.pos[0] - r * sin(this.rot);
        var cy = this.pos[1] - r * cos(this.rot);
        this.tc = [cx, cy];
        for (var i = 0; i < this.tpa; i++) {
            var xp = cx + r * sin(this.rot + tan(this.fw_ang) * i * signof(speed) * 0.3);
            var yp = cy + r * cos(this.rot + tan(this.fw_ang) * i * signof(speed) * 0.3);
            if (this.world.get_terrain([xp, yp])) {
                break;
            }
            this.tp[i] = [xp, yp];
        }
    }
}

function radians(x) {
    return x * (Math.PI / 180);
}

function signof(x) {
    if (x == 0)
        return 0;
    else
        return x / Math.abs(x);
}

function min(x) {
    return Math.min(x);
}

function max(x) {
    return Math.max(x);
}

function atan2(y, x) {
    return Math.atan2(y, x);
}

function int(x) {
    return parseInt(x);
}

function float(x) {
    return parseFloat(x);
}

function tan(x) {
    return Math.tan(x);
}

function between(val, minv, maxv) {
    if (val < minv)
        return minv;
    if (val > maxv)
        return maxv;
    return val;
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