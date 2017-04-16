/**
 * Created by chiajun on 2/8/17.
 */


var imgCache = [],
    canvas,
    gardenInstance,
    gridSize = 100;

/**
 * Setup csrftoken for ajax queries.
 */
function setupCSRF() {
    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

}

/**
 * Make sure objects on the canvas move within the bound of the canvas.
 */
function fixCanvasBound() {
    // Limit the border of the canvas
    canvas.on('object:moving', function (e) {
            var obj = e.target;
            // if object is too big ignore
            if (obj.currentHeight > obj.canvas.height || obj.currentWidth > obj.canvas.width) {
                return;
            }
            obj.setCoords();
            // top-left  corner
            if (obj.getBoundingRect().top < 0 || obj.getBoundingRect().left < 0) {
                obj.top = Math.max(obj.top, obj.top - obj.getBoundingRect().top);
                obj.left = Math.max(obj.left, obj.left - obj.getBoundingRect().left);
            }
            // bot-right corner
            if (obj.getBoundingRect().top + obj.getBoundingRect().height > obj.canvas.height || obj.getBoundingRect().left + obj.getBoundingRect().width > obj.canvas.width) {
                obj.top = Math.min(obj.top, obj.canvas.height - obj.getBoundingRect().height + obj.top - obj.getBoundingRect().top);
                obj.left = Math.min(obj.left, obj.canvas.width - obj.getBoundingRect().width + obj.left - obj.getBoundingRect().left);
            }

            e.target.set({
                left: calSnapOffset(e.target.left),
                top: calSnapOffset(e.target.top)
            }).setCoords();
        }
    );
}

/**
 * Toggle the draw button and allow users to draw on canvas
 * (Doesn't work on touch screen)
 */
function draw() {
    canvas.isDrawingMode = !canvas.isDrawingMode;
    if (canvas.freeDrawingBrush) {
        canvas.freeDrawingBrush.color = "red";
        canvas.freeDrawingBrush.shadowBlur = 0;
    }

    if (canvas.isDrawingMode)
        $('#drawBtn').text("Cancel");
    else
        $('#drawBtn').text("Draw");

}

/**
 * Save the changes bed plan into the database according to the bed name
 */
function saveImage() {
    var canvasData = JSON.stringify(canvas);
    $.ajax({
        url: "/saveImage/",
        type: "POST",
        data: {
            bedName: "Venus",
            canvasData: canvasData
        },
        success: function (data) {
            console.log(data);
        },
        error: function (xhr, errmsg, err) {
            console.log("Error: " + errmsg);
        }
    }).done(function (data) {
        alert("Save successfully.")
    });
}

/**
 * Load the bed plan based on the bed's name
 */
function loadImage() {
    $.ajax({
        url: "/loadImage",
        type: "GET",
        data: {
            bedName: "Venus"
        },
        success: function (data) {
            canvas.loadFromJSON(data, canvas.renderAll.bind(canvas));
        },
        error: function (xhr, errmsg, err) {
            console.log("Error: " + errmsg);
        }
    });
}

/**
 * Remove the selected object from the canvas
 */
function eraseObj() {
    if (canvas.getActiveObject() != null) {
        imgCache.push(canvas.getActiveObject());
        canvas.getActiveObject().remove();
    }
}

/**
 * Remove last added object from the canvas
 */
function removeLastObj() {
    var obj = canvas.getObjects();
    if (obj.length > 1) {
        var lastObj = obj[obj.length - 1];
        imgCache.push(lastObj);
        canvas.remove(lastObj);
    }
}

/**
 * Restore the last removed object and load it on the canvas.
 */
function restoreLastObj() {
    if (imgCache.length > 0)
        canvas.add(imgCache.pop());
}

/**
 * Draw the griz based on the given grid size.
 */
function drawGrid() {
    for (var x = 1; x < (canvas.getWidth() / gridSize); x++) {
        canvas.add(new fabric.Line([gridSize * x, 0, gridSize * x, canvas.getWidth()], {
            stroke: "#000000",
            strokeWidth: 1,
            selectable: false,
            strokeDashArray: [5, 5]
        }));
        canvas.add(new fabric.Line([0, gridSize * x, canvas.getWidth(), gridSize * x], {
            stroke: "#000000",
            strokeWidth: 1,
            selectable: false,
            strokeDashArray: [5, 5]
        }));
    }
}

/**
 *  Calculate the snapping offset by the given position of x or y.
 * @param pos
 * @returns {number}
 */
function calSnapOffset(pos) {
    return Math.round(pos / gridSize) * gridSize;
}

/**
 * Initialize all garden canvas and make them to be draggable
 */
function initGardenItems() {
    // target elements with the "draggable" class
    $('.gardenItems').draggable({
        helper: "clone"
    });

    $('#gardenCanvas').droppable({
        accept: ".gardenItems",
        drop: function (event, ui) {
            var imgSrc = ui.draggable.context.getAttribute("src"),
                offLeft = $(this).offset().left,
                offTop = $(this).offset().top;

            fabric.Image.fromURL(imgSrc, function (img) {
                img.scaleToWidth(gridSize);
                img.scaleToHeight(gridSize);
                img.left = calSnapOffset(ui.position.left - offLeft);
                img.top = calSnapOffset(ui.position.top - offTop);
                canvas.add(img);
            });
        }
    });
}

$(document).ready(function () {
    var clearBtn = document.getElementById("clrBtn"),
        resetBtn = document.getElementById("resetBtn"),
        undoBtn = document.getElementById("undoBtn"),
        redoBtn = document.getElementById("redoBtn"),
        drawImage = document.getElementById("drawBtn"),
        saveImageBtn = document.getElementById("saveImg"),
        loadImageBtn = document.getElementById("loadImg");

    gardenInstance = new fabric.Image.fromURL("/static/img/gardenPlan.jpg", function (img) {
        img.scaleToWidth(canvas.getWidth());
        img.scaleToHeight(canvas.getHeight());
        img.selectable = false;
        // canvas.add(img);
        gardenInstance = img;
    });
    canvas = new fabric.Canvas('gardenCanvas');
    fixCanvasBound();
    drawGrid();
    setupCSRF();

    // Attach drawing event
    drawImage.onclick = function () {
        draw();
    };

    // Attach save image event
    saveImageBtn.onclick = function () {
        saveImage();
    };

    loadImageBtn.onclick = function () {
        loadImage();
    };

    clearBtn.onclick = function () {
        eraseObj();
    };

    resetBtn.onclick = function () {
        canvas.clear();
        canvas.add(gardenInstance);
    };

    undoBtn.onclick = function () {
        removeLastObj();
    };

    redoBtn.onclick = function () {
        restoreLastObj();
    };

    // Initialize the garden items
    initGardenItems();
});



