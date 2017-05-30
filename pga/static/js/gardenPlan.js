/**
 * Created by chiajun on 2/8/17.
 */


var imgCache = [],
    canvas,
    gardenInstance,
    gridSize = 50;


var gardenName;
var existingPlanName = "";
var isExistingPlan = false;
var existingPlanId = -1;

/**
 * Setup csrftoken for ajax queries.
 */
function setupCSRF() {
    // CSRF code
    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
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
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
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
        $('#drawBtn').text("Stop Drawing");
    else
        $('#drawBtn').text("Draw");
}

/**
 * Save the changes bed plan into the database according to the bed name
 */
function savePlan() {
    var bedCanvas = JSON.stringify(canvas),
        bedPlan = $('#bedPlanName').val(),
        gardenTitle = $('#gardenTitle').html(),
        bedName = gardenTitle.substr(0, gardenTitle.indexOf('\'s'));
    $.ajax({
        url: "/savePlan/",
        type: "POST",
        data: {
            bedName: bedName,
            bedPlan: bedPlan,
            bedCanvas: bedCanvas
        },
        success: function (data) {
            alert("Saved successfully.");

            var username = data['username'];
            existingPlanId = data['plan_id'];

            var curDate = new Date().toLocaleString();

            isExistingPlan = true;
            existingPlanName = bedPlan;
            toggleButtons();

            $("#createDetails").text(existingPlanName + ", created by " + username + " at " + curDate);
            $("#lastUpdate").text("Last update at " + curDate + " by " + username);
        },
        error: function (xhr, errmsg, err) {
            console.log("Error: " + errmsg);
        }
    });
}

function updateExistingPlan() {
    var bedCanvas = JSON.stringify(canvas);

    $.ajax({
        url: "/updatePlan/",
        type: "POST",
        data: {
            plan_id: existingPlanId,
            canvas: bedCanvas
        },
        success: function (data) {
            alert("Updated successfully.");
            var username = data['username'];
            var curDate = new Date().toLocaleString();
            $("#lastUpdate").text("Last update at " + curDate + " by " + username);
        },
        error: function (xhr, errmsg, err) {
            console.log("Error: " + errmsg);
        }
    });
}

/**
 * Remove the selected bed plan
 * @param planID
 */
function deletePlan(planID) {
    $.ajax({
        url: "/deletePlan/",
        type: "POST",
        data: {
            planID: planID
        },
        success: function (data) {
            document.getElementById(planID).remove();
        },
        error: function (xhr, errmsg, err) {
            console.log("Error: " + errmsg);
        }
    });
}

/**
 * Change the selected plan into be active class
 * @param el
 */
function setSelectedPlan(el) {
    $(el).parent().find('a').removeClass('active');
    $(el).addClass('active');
}

/**
 * Display all bed plans for the current garden
 */
function showPlans() {

    $.ajax({
        url: "/showPlans",
        type: "GET",
        data: {
            bedName: gardenName
        },
        success: function (resp) {
            var plans = resp.context;
            $("#plansList a").remove();
            for (var i = 0; i < plans.length; i++) {
                var bedPlan = plans[i].bedPlan,
                    planID = plans[i].planID;
                $("#plansList").append('<a href="#" id= ' + planID + ' class="list-group-item" onclick="setSelectedPlan(this)">' + bedPlan + '<button type="button" class="close float-right deletePlanX" aria-label="Close" onclick="deletePlan(' + planID + ')"> <span aria-hidden="true">&times;</span> </button></a>');
            }
        },
        error: function (xhr, errmsg, err) {
            alert("Error: " + errmsg);
        }
    });
}

/**
 * Load the selected bed plan into canvas.
 */
function loadPlan() {
    var selectedPlan = document.getElementsByClassName("list-group-item active")[0],
        selectedPlanID = selectedPlan.id;

    $.ajax({
        url: "/getBedCanvas",
        type: "GET",
        data: {
            planID: selectedPlanID
        },
        success: function (resp) {
            var canvasData = resp['canvas'];
            var planData = resp['data'];

            var planName = planData['plan_name'];
            existingPlanName = planName;
            var username = planData['created_by'];
            var createDateStr = planData['created_date'];
            var createDate = new Date(createDateStr);

            var updateDateStr = planData['updated_date'];
            var updateDate = new Date(updateDateStr);
            var updatedBy = planData['updated_by']

            isExistingPlan = true;
            existingPlanId = selectedPlanID
            toggleButtons();

            $("#createDetails").text(planName + ", created by " + username + " at " + createDate.toLocaleString());
            $("#lastUpdate").text("Last update at " + updateDate.toLocaleString() + " by " + updatedBy);
            canvas.loadFromJSON(JSON.parse(canvasData), canvas.renderAll.bind(canvas));
            drawGrid();
        },
        error: function (xhr, errmsg, err) {
            alert("Error: " + errmsg);
            console.log(err);
        }
    });
}

function markAsCurrent(){
    $.ajax({
        url: "/markCurrent/",
        type: "POST",
        data: {
            plan_id: existingPlanId,
            bed_name: gardenName
        },
        success: function (data) {
            alert("This plan is now the 'As Planted' plan for this garden. Go back and select 'Current Plan' to view it. It is no longer editable.")
        },
        error: function (xhr, errmsg, err) {
            console.log("Error: " + errmsg);
        }
    });
}

function toggleButtons() {
    $("#updatePlan").toggle(isExistingPlan);
    $("#makeCurrentBtn").toggle(isExistingPlan);
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
            var imgSrc = ui.draggable.context.getAttribute("src");

            fabric.Image.fromURL(imgSrc, function (img) {
                img.scaleToWidth(gridSize);
                img.scaleToHeight(gridSize);
                var pointer = canvas.getPointer(event);
                img.left = Math.floor(pointer.x / gridSize) * gridSize;
                img.top = Math.floor(pointer.y / gridSize) * gridSize;
                canvas.add(img);
                canvas.sendToBack(img);
            });
        }
    });

    $("#gridInput").val(50);
}

function changeGridSize() {
    gridSize = Math.round($("#gridInput").val());
    $("#gridInput").val(gridSize)
    resetCanvas();
    drawGrid();
}

function timeStamp() {
    // Create a date object with the current time
    var now = new Date();
    // Create an array with the current month, day and time
    var date = [now.getMonth() + 1, now.getDate(), now.getFullYear()];
    // Create an array with the current hour, minute and second
    var time = [now.getHours(), now.getMinutes(), now.getSeconds()];
    // Determine AM or PM suffix based on the hour
    var suffix = ( time[0] < 12 ) ? "AM" : "PM";
    // Convert hour from military time
    time[0] = ( time[0] < 12 ) ? time[0] : time[0] - 12;
    // If hour is 0, set it to 12
    time[0] = time[0] || 12;

    // If seconds and minutes are less than 10, add a zero
    for (var i = 1; i < 3; i++) {
        if (time[i] < 10) {
            time[i] = "0" + time[i];
        }
    }
    // Return the formatted string
    return date.join("/") + " " + time.join(":") + " " + suffix;
}

function resetCanvas() {
    canvas.clear();
    drawGrid();
    isExistingPlan = false;
    existingPlanName = "";
    existingPlanId = -1;
    toggleButtons();
    $("#createDetails").text("New plan");
    $("#lastUpdate").text("");
}

$(document).ready(function () {
    var resetBtn = document.getElementById("resetBtn"),
        savePlan = document.getElementById("savePlan");

    gardenName = $("#gardenName").val();

    gardenInstance = new fabric.Image.fromURL("/static/img/gardenPlan.jpg", function (img) {
        img.scaleToWidth(canvas.getWidth());
        img.scaleToHeight(canvas.getHeight());
        img.selectable = false;
        // canvas.add(img);
        gardenInstance = img;
    });
    canvas = new fabric.Canvas('gardenCanvas');
    canvas.setHeight(window.innerHeight / 2);
    canvas.setWidth($(".toolbar").width());
    fixCanvasBound();
    drawGrid();
    setupCSRF();

    savePlan.onclick = function () {
        $('#bedPlanName').val(timeStamp());
    };

    // Initialize the garden items
    initGardenItems();

    $(".ui-loader").hide();

    $("#updatePlan").click(updateExistingPlan);
    $("#confirmMarkCurrentBtn").click(markAsCurrent);

    $("#updatePlan").toggle();
    $("#makeCurrentBtn").toggle();
});



