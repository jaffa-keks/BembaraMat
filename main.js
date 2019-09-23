var canvas, display;
var running, size;
var world, ui;
var clock;
var input;

var drawCol = "black";

function update() {
    world.update();
}

function render() {
    //background
    //display.fillStyle = "black";
    //display.fillRect(0, 0, canvas.width, canvas.height);
    world.render(display);
    //ui.render(display);
}

function on_loop() {
    update();
    render();
}

function init_sim() {
    
    var level_img = new Image();
    input = new Input();
    level_img.src = "./../src/world1.png";
    level_img.onload = function() {
        canvas.width = this.width;
        canvas.height = this.height;
        keys();
        world = new World(input, get_terr_data(this));
        clock = setInterval(on_loop, 30);
    };
    //on_loop();
}

function init_from_edit(data) {
    input = new Input();
    keys();
    console.log(data);
    world = new World(input, data);
    clock = setInterval(on_loop, 30);
}

function init_lvl_edit() {
    $(document).keydown(function(e) {
        if (e.which == 68)
            drawCol = "black";
        if (e.which == 69)
            drawCol = "white";
    });
    display.clearRect(0, 0, canvas.width, canvas.height);
    canvas.addEventListener("mousemove", draw_on_move, false);
    $("#start").click(function() {
        init_from_edit(display.getImageData(0, 0, canvas.width, canvas.height));
        $(this).hide();
    });
}

function mouse_pos(evt) {
    var rect = canvas.getBoundingClientRect();
    return [evt.clientX - rect.left, evt.clientY - rect.top];
}

function draw_on_move(evt) {
    if (evt.buttons != 1)
        return;
    display.beginPath();
    var mp = mouse_pos(evt);
    display.arc(mp[0], mp[1], 10, 0, 2 * Math.PI);
    display.fillStyle = drawCol;
    display.fill();
}

function keys() {
    $(document).keydown(function(e) {
        switch(e.which) {
            case 37: // left
                input.hor = -1;
            break;    
            case 38: // up
                input.ver = -1;
            break;    
            case 39: // right
                input.hor = 1;
            break;    
            case 40: // down
                input.ver = 1;
            break;
            default: return; // exit this handler for other keys
        }
        e.preventDefault(); // prevent the default action (scroll / move caret)
    });
    $(document).keyup(function(e) {
        switch(e.which) {
            case 37: // left
                input.hor = 0;
            break;    
            case 38: // up
                input.ver = 0;
            break;    
            case 39: // right
                input.hor = 0;
            break;    
            case 40: // down
                input.ver = 0;
            break;    
            default: return; // exit this handler for other keys
        }
    });
}

function get_terr_data(image_data) {
    var c = document.createElement("canvas");
    c.width = image_data.width;
    c.height = image_data.height;
    var ct = c.getContext("2d");
    ct.drawImage(image_data, 0, 0);
    var idata = ct.getImageData(0, 0, image_data.width, image_data.height);
    return idata;
}

function extract_alpha(image_data) {
    var temp = [];
    var idata = image_data.data;
    for (var i = 3; i < idata.length; i += 4) {
        temp.push(idata[i]);
    }
    return temp;
}

$(document).ready(function() {
    canvas = document.getElementById("display");
    canvas.width = $("#display").width();
    canvas.height = $("#display").height();
    display = canvas.getContext("2d");
    init_lvl_edit();
});