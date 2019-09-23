class World {
    constructor(input, data) {
        this.lvl_img = data;
        this.width = data.width;
        this.height = data.height;
        this.terr_data = extract_alpha(data);
        this.car = new Car(this, input);
    }

    update() {
        this.car.update();
    }

    render(display) {
        display.putImageData(this.lvl_img, 0, 0);
        this.car.render(display);
    }

    get_terrain(point) {
        if (point[0] < 0 || point[0] >= this.width)
            return true;
        if (point[1] < 0 || point[1] >= this.height)
            return true;
        var pa = this.terr_data[parseInt(point[0]) + parseInt(point[1]) * this.width];
        return pa == 255 ? true : false;
    }
}
