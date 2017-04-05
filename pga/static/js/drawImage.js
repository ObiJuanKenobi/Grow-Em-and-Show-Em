/**
 * Created by chiajun on 2/8/17.
 */


var imgCache = [],
    canvas,
    gardenInstance,
    itemsCanvas,
    draggedInstance;

var fixCanvasBound = function () {
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
    });
};

var draw = function () {
    canvas.isDrawingMode = !canvas.isDrawingMode;
    if (canvas.freeDrawingBrush) {
        canvas.freeDrawingBrush.color = "red";
        canvas.freeDrawingBrush.shadowBlur = 0;
    }

    if (canvas.isDrawingMode)
        $('#drawBtn').text("Cancel");
    else
        $('#drawBtn').text("Draw");

};

var saveImage = function () {
    var dataUrl = canvas.toDataURL('gardenImage.png');
    var imageData = canvas.toDatalessJSON();
    $.ajax({
        url: "/saveImage",
        type: "GET",
        data: {fileName: "gardenPlan.jpg", imageData: imageData}
    }).done(function (data) {
        console.log("Success");
    });
};

var eraseObj = function () {
    if (canvas.getActiveObject() != null) {
        imgCache.push(canvas.getActiveObject());
        canvas.getActiveObject().remove();
    }
};

var removeLastObj = function () {
    var obj = canvas.getObjects();
    if (obj.length > 1) {
        var lastObj = obj[obj.length - 1];
        imgCache.push(lastObj);
        canvas.remove(lastObj);
    }
};

var restoreLastObj = function () {
    if (imgCache.length > 0)
        canvas.add(imgCache.pop());
};

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("src", ev.target.src);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("src");
    fabric.Image.fromURL(data, function (img) {
        img.scaleToWidth(Math.round(canvas.getWidth() * 0.2));
        img.scaleToHeight(Math.round(canvas.getHeight() * 0.2));
        canvas.add(img);
    });
}

var initGardenItems = function () {
    var elements = $(".gardenItems");

    interact(".gardenLayout").dropzone({
        accept: ".gardenItems",
        overlap: 0.75,
        ondropactivate: function (event) {
            // add active dropzone feedback
            event.target.classList.add('drop-active');
        },
        ondragenter: function (event) {
            var draggableElement = event.relatedTarget,
                dropzoneElement = event.target;

            // feedback the possibility of a drop
            dropzoneElement.classList.add('drop-target');
        },
        ondragleave: function (event) {
            // remove the drop feedback style
            event.target.classList.remove('drop-target');
        },
        ondrop: function (event) {
            canvas.add(draggedInstance);
        },
        ondropdeactivate: function (event) {
            // remove active dropzone feedback
            event.target.classList.remove('drop-active');
            event.target.classList.remove('drop-target');
        }
    });

    // for (var i = 0; i < elements.length; i++) {
    //     interact(elements[i]).draggable({
    //         snap: {
    //             targets: [
    //                 interact.createSnapGrid({x: 10, y: 10})
    //             ],
    //             range: Infinity,
    //             relativePoints: [{x: 0, y: 0}]
    //         },
    //         inertia: true,
    //         restrict: {
    //             restriction: document.getElementById("gardenCanvas"),
    //             elementRect: {top: 0, left: 0, bottom: 1, right: 1},
    //             endOnly: true
    //         }
    //     }).on('dragmove', function (event) {
    //         var target = event.target,
    //             x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx,
    //             y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;
    //         event.target.style.webkitTransform =
    //             event.target.style.transform =
    //                 'translate(' + x + 'px, ' + y + 'px)';
    //         // update the posiion attributes
    //         target.setAttribute('data-x', x);
    //         target.setAttribute('data-y', y);
    //     });
    // }
};

$(document).ready(function () {
    var clearBtn = document.getElementById("clrBtn");
    var resetBtn = document.getElementById("resetBtn");
    var undoBtn = document.getElementById("undoBtn");
    var redoBtn = document.getElementById("redoBtn");
    gardenInstance = new fabric.Image.fromURL("/static/img/gardenPlan.jpg", function (img) {
        img.scaleToWidth(canvas.getWidth());
        img.scaleToHeight(canvas.getHeight());
        img.selectable = false;
        canvas.add(img);
        gardenInstance = img;
    });
    canvas = new fabric.Canvas('gardenCanvas');
    var drawImage = $('#drawBtn')[0];
    var saveImageBtn = $('#saveImg')[0];
    fixCanvasBound();

    // Attach drawing event
    drawImage.onclick = function () {
        draw();
    };

    // Attach save image event
    saveImageBtn.onclick = function () {
        saveImage();
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



