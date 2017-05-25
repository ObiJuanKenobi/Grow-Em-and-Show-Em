

function saveChangedQuestions(){
    //Save was pressed, find text that changed and update DB
    $("#questionsDiv div").each(function() {
        var id = $(this).attr('id');
        id = id.replace("question", ""); // Turns 'question19' into '19'
        var originalText = $(this).find(".questionText").text().trim();
        var editedText = String($(this).find(".questionTextEdit").val()).trim();

        if(originalText !== editedText){
            alert("New question: " + editedText + ", " + originalText + ", " + id);

            updateQuestion(id, editedText);
        }

        $(this).find("ol li").each(function() {
            var answerId = $(this).attr('id');
            answerId = answerId.replace("answer", "");
            var originalAnswer = $(this).find(".answer").text().trim();
            var editedAnswer = String($(this).find(".answerEdit").val()).trim();
            var name = 'correct' + id;
            var isCorrect = $(this).find("input[name=" + name + "]").is(":checked");
            var wasCorrect = $(this).find("span").hasClass("correct");

            if(originalAnswer !== editedAnswer){
                //alert("New answer: " + editedAnswer + " , id: " + answerId + ", isCorrect: " + isCorrect);
                updateAnswer(answerId, editedAnswer, isCorrect);
            }
            else if( isCorrect !== wasCorrect){
                //alert("Answer didn't change, but correctness did");
                updateAnswer(answerId, editedAnswer, isCorrect);
            }

        });
    });
}

function updateQuestion(id, editedText){
    $.ajax({
        url: "/pgaadmin/quiz/editQuestion",
        type: "POST",
        data: {
            questionid: id,
            newquestion: editedText
        },
        success: function (data) {
            //alert("Success!");
            console.log(data);
        },
        error: function (xhr, errmsg, err) {
            alert("Error: " + errmsg);
            console.log(errmsg);
        }
    });
}

function updateAnswer(answerId, newAnswer, isCorrect){
    $.ajax({
        url: "/pgaadmin/quiz/editAnswer",
        type: "POST",
        data: {
            answerid: answerId,
            newanswer: newAnswer,
            iscorrect: isCorrect
        },
        success: function (data) {
            //alert("Success!");
            console.log(data);
        },
        error: function (xhr, errmsg, err) {
            alert("Error: " + errmsg);
            console.log(errmsg);
        }
    });
}

var editing = false;
var uploadDialog;
var fileUploadId;

var uploadNewQuizFile = function() {
    var file = document.getElementById(fileUploadId).files[0];
    //alert(file.name);

    var uploadType = $('input[name=uploadType]:checked').val();
    //alert(uploadType);

    $("#uploadForm").submit();

    uploadDialog.dialog("close");
};

var clearAddDialog = function() {
    $(".extra-answer").remove();
    $(".addQuestionAnswer").val("");
    $("#addQuestionTitle").val("");
    addDialog.dialog("close");
};

var addDialog;
var addQuestion = function() {
    var title = $("#addQuestionTitle").val();

    var answers = [];
    $(".addQuestionAnswer").each(function() {
        var answer = $(this).val();
        answers.push(answer);
    });

    var correct_answer = $("#correctAnswerSelect option:selected").val();

    var unit = $("#currentUnit").val();

    $.ajax({
        url: "/pgaadmin/quiz/addQuestion",
        type: "POST",
        data: {
            question: title,
            'answers[]': answers,
            correct: correct_answer,
            course: unit
        },
        success: function (data) {
            //alert("Success!");
            console.log(data);
        },
        error: function (xhr, errmsg, err) {
            alert("Error: " + errmsg);
            console.log(errmsg);
        }
    });

    clearAddDialog();
}

$(function() {

    setupCSRF();
    fileUploadId = $("#fileUploadId").val();

    addDialog = $("#addQuestionDialog").dialog({
        autoOpen: false,
        height: 400,
        width: 650,
        modal: true,
        buttons: [
            {
              id: "cancel",
              text: "Cancel",
              click: clearAddDialog
            },
            {
                id: "addQuestionBtn",
                text: "Add",
                click: addQuestion
            }
        ]
     });

    uploadDialog = createUploadDialog(fileUploadId);

    $("#uploadListBtn").click(function(){
        $("#uploadHelpText").text("(Expects an Excel or CSV file)");
        uploadDialog.dialog("open");
    });

    $("#editBtn").click(function() {

        $(".questionText").toggle();
        $(".questionTextEdit").toggle();
        $(".answerEdit").toggle();
        $(".answer").toggle();
        $(".correctOption").toggle();
        $(".deleteBtn").toggle();

        editing = !editing;

        if(editing){
            $("#editBtn").text('Save');
        }
        else {
            $("#editBtn").text('Edit');

            saveChangedQuestions();
        }
    });

    $(".deleteBtn").click(function() {
        var id = $(this).attr('id');
        id = id.replace("delete", "");

        $.ajax({
            url: "/pgaadmin/quiz/deleteQuestion",
            type: "POST",
            data: {
                questionId: id
            },
            success: function (data) {
                //alert("Success!");
                console.log(data);
            },
            error: function (xhr, errmsg, err) {
                alert("Error: " + errmsg);
                console.log(errmsg);
            }
        });
    });

    $("#addBtn").click(function() {
        addDialog.dialog("open");
    });

    $("#addAnswerBtn").click(function() {
        var answerNum = $("#correctAnswerSelect option").length + 1;
        var newLabel = $("<label>").text("Answer " + answerNum + ": ").addClass("extra-answer");
        var newInput = $("<input>").attr('type', 'text')
                                   .attr('size', '50')
                                   .addClass('addQuestionAnswer')
                                   .appendTo(newLabel);
        newLabel.append("<br>");

        $("#addQuestionAnswers").append(newLabel);

        var newOption = $("<option>").val(answerNum).text(answerNum).addClass("extra-answer");
        $("#correctAnswerSelect").append(newOption);
    })

});