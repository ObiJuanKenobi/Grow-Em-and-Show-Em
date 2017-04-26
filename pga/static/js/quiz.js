$(function(){
    setupCSRF();
    
    $("#submitBtn").click(function() {
        var results = getAnswers()
        submitQuiz(results.q, results.a);
        // if(results.length == 0){
            // quizPassed();
        // }
        // else {
            // quizFailed(results);
        // }
    });
});

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

function getAnswers() {
    var questions = [];
    var answers = [];
    
    $(".questionDiv").each(function(index) {
        var correct_answer = $(this).find('.answer').val();
        //I didn't want to use just id # since a question & answer could possibly have same id's
        var questionId = $(this).attr('id').replace('question', ''); 
        //var users_answer = $(this).find("input[name='" + questionId + "']:checked").val();
        var users_answer = $(this).find("input[name='" + questionId + "']:checked").attr('id').replace('answer', '');
        
        questions.push(questionId);
        answers.push(users_answer);
        
        // var correct = correct_answer === users_answer;
        // if(!correct){
            // results.push({"question": questionId, "correct": correct_answer});
        // }
    });
    console.log(questions, answers);
    return { q: questions, a: answers };
}

function submitQuiz(questionsArr, answersArr){
    var courseTitle = $(".unitTitle").attr('id');
    console.log(courseTitle);
    $.ajax({
        url: "/gradeQuiz/" + courseTitle,
        type: "POST",
        data: {
            'questions[]': questionsArr,
            'answers[]': answersArr
        },
        success: function (data) {
            console.log(data);
            if(data.passed){
                window.location.href = data.redirect_url;
            }
            else {
                
                var num_wrong = 0;
                var results = data.results;
                for(var i=0; i<results.length; i++){
                    var qResult = JSON.parse(results[i]);
                    if(!qResult.user_correct){
                        num_wrong++;
                        
                        var qId = qResult.question_id;
                        var aId = qResult.answer_id;
                        
                        var htmlQid = "#question" + String(qId);
                        var htmlAid = "#answerLabel" + String(aId);
                        console.log(htmlAid);
                        $(htmlAid).css("color", "red");
                    }
                }
                
                var questionsStr = "questions";
                if (num_wrong == 1){
                    questionsStr = "question";
                }
                $("#quizStatus").text("You did not pass the quiz. You missed " + String(num_wrong) + " " + questionsStr + ". Correct answers are shown in red. Spend more time reviewing lessons, or click 'Retake' to try again.");
                
                $("#submitBtn").val("Retake");
                $("#submitBtn").off("click");
                $("#submitBtn").wrap("<a href='" + data.redirect_url + "'></a>")
                
                jQuery('html,body').animate({scrollTop:0},0);
            }
        },
        error: function (xhr, errmsg, err) {
            alert("Error: " + errmsg);
            console.log(errmsg);
        }
    });
}

function quizFailed(results) {
    var msg = "You did not pass the quiz! Missed " + results.length + " questions.";
    alert(msg);
    
    for(var i=0; i<results.length; i++){
        var qId = results[i].question;
        var correctOption = results[i].correct;
        $("#" + qId + " ." + correctOption).css("color", "red");
    }
    
    var extraAttempts = 3; //GET from DB
    
    if(extraAttempts > 0) {
        $("#submitBtn").val("Try Again");
        $("#submitBtn").click(function() {
            alert("TODO - load new quiz questions, add failed attempt to DB for user");
            $("#submitBtn").val("Submit Answers");
        });
    }
    else {
        //Redirect to lessons?
    }
}