/**
 * Created by chiajun on 2/8/17.
 */

var imgCache = [];

var fixCanvasBound = function (canvas) {
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

var draw = function (canvas) {
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

var saveImage = function (canvas) {
    var dataUrl = canvas.toDataURL('gardenImage.png');
    var imageData = canvas.toDatalessJSON();
    $.ajax({
        url: "/saveImage",
        type: "GET",
        data: {fileName: "gardenPlan.jpg", imageData: imageData}
    }).done(function(data){
        console.log("Success");
    });
};

var eraseObj = function (canvas) {
    if (canvas.getActiveObject() != null) {
        imgCache.push(canvas.getActiveObject());
        canvas.getActiveObject().remove();
    }
};

var removeLastObj = function (canvas) {
    var obj = canvas.getObjects();
    if(obj.length > 1){
        var lastObj = obj[obj.length - 1];
        imgCache.push(lastObj);
        canvas.remove(lastObj);
    }
};

var restoreLastObj = function (canvas) {
    if(imgCache.length > 0)
        canvas.add(imgCache.pop());
};

$(document).ready(function () {
    var clearBtn = document.getElementById("clrBtn");
    var gardenImg = document.getElementById("garden");
    var resetBtn = document.getElementById("resetBtn");
    var undoBtn = document.getElementById("undoBtn");
    var redoBtn = document.getElementById("redoBtn");
    var gardenInstance = new fabric.Image(gardenImg);
    var canvas = new fabric.Canvas('gardenCanvas');
    var drawImage = $('#drawBtn')[0];
    var saveImageBtn = $('#saveImg')[0];

    gardenInstance.scaleToWidth(canvas.getWidth());
    gardenInstance.scaleToHeight(canvas.getHeight());
    gardenInstance.selectable = false;
    canvas.add(gardenInstance);
    gardenInstance.center();
    fixCanvasBound(canvas);

    // Attach drawing event
    drawImage.onclick = function () {
        draw(canvas);
    };

    // Attach save image event
    saveImageBtn.onclick = function () {
        saveImage(canvas);
    };

    clearBtn.onclick = function () {
        eraseObj(canvas);
    };

    resetBtn.onclick = function () {
        canvas.clear();
        canvas.add(gardenInstance);
        gardenInstance.center();
    };

    undoBtn.onclick = function () {
        removeLastObj(canvas);
    };
    
    redoBtn.onclick = function () {
        restoreLastObj(canvas);
    };
});



