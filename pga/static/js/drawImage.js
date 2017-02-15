/**
 * Created by chiajun on 2/8/17.
 */

$(document).ready(function () {
    var gardenImg = document.getElementById("garden");
    var gardenInstance = new fabric.Image(gardenImg);
    var canvas = new fabric.Canvas('gardenCanvas');
    gardenInstance.scaleToWidth(canvas.getWidth());
    gardenInstance.scaleToHeight(canvas.getHeight());
    canvas.add(gardenInstance);

    // Limit the border of the canvas
    canvas.on('object:moving', function (e) {
       var obj = e.target;
         // if object is too big ignore
        if(obj.currentHeight > obj.canvas.height || obj.currentWidth > obj.canvas.width){
            return;
        }
        obj.setCoords();
        // top-left  corner
        if(obj.getBoundingRect().top < 0 || obj.getBoundingRect().left < 0){
            obj.top = Math.max(obj.top, obj.top-obj.getBoundingRect().top);
            obj.left = Math.max(obj.left, obj.left-obj.getBoundingRect().left);
        }
        // bot-right corner
        if(obj.getBoundingRect().top+obj.getBoundingRect().height  > obj.canvas.height || obj.getBoundingRect().left+obj.getBoundingRect().width  > obj.canvas.width){
            obj.top = Math.min(obj.top, obj.canvas.height-obj.getBoundingRect().height+obj.top-obj.getBoundingRect().top);
            obj.left = Math.min(obj.left, obj.canvas.width-obj.getBoundingRect().width+obj.left-obj.getBoundingRect().left);
        }
    });




});
