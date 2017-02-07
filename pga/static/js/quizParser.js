/** This code is used to parse the questions file
 pick random questions, and perform scoring once 
 answers are submitted 
 
 Author: Jacob S
*/
 
var NUM_QUESTIONS_PER_QUIZ = 5;
 
var quizQuestions;

/*
	Given a file path to a JSON file,
		this function will parse in into an array of 
		multiple choice questions, pick random ones,
		and display them on th html page
	Expects input to be in form:
	[
		{
			question: "What is..",
			optionA: "X",
			optionB: "Y",
			optionC: "Z",
			optionD: "W",
			correct: "a" / b / c / d
		}
	]
*/
var initQuiz = function(quizFilePath) {
	quizFilePath = "static/quizzes/defaultQuiz.json";
	
	$.ajax({
		url: quizFilePath,
		dataType: 'json',
		success: function(data){
			console.log(JSON.stringify(data));
			getRandomQuestions(data);
			displayQuestions();
		},
		error: function(xhr, status, error){
			alert("Error loading quiz questions");
		}
	});
};

/*
	Takes as input the entrie array of quiz questions,
	and uniformaly randomly selects and assigns them
	to the quizQuestions array
*/
var getRandomQuestions = function(json){
	quizQuestions = [];
	
	var totalNumQuestions = json.length;
	
	//Init a boolean array to all false:
	var taken = Array.apply(null, Array(totalNumQuestions)).map(function() { return false });
	
	var numPicked = 0;
	while(numPicked < NUM_QUESTIONS_PER_QUIZ) {
		var rand = Math.floor(Math.random() * totalNumQuestions);
		
		if(!taken[rand]){
			quizQuestions.push(json[rand]);
			taken[rand] = true;
			numPicked++;
		}
	}
};

/*
 Takes as input an array ['a', 'b', 'c', ...]
 Returns array of { number: x, correct: "" } objects,
 One for each wrong answer (so empty array if all correct)
*/
var gradeAnswers = function(answers){
	
	var results = [];
	
	for(var i=0; i<answers.length; i++){
		if(answers[i] !== quizQuestions[i].correct){
			results.push({ "number": i+1, "correct": quizQuestions[i].correct });
		}
	}
	
	return results;
}

/*
 Populates the HTML page with the questions content
*/
var displayQuestions = function() {
	
	for(var i=0; i<quizQuestions.length; i++){
		
		var qNum = i + 1;
		var questionObj = quizQuestions[i];
		
		var div = document.getElementById('q' + qNum);
		
		var innerHtml = "<b>Question " + qNum + ". </b>" + questionObj.question + "<br>" +
			"<input type='radio' value='a' name='q2'> a. " + questionObj.a + "<br>" + 
			"<input type='radio' value='b' name='q2'> b. " + questionObj.b + "<br>" + 
			"<input type='radio' value='c' name='q2'> c. " + questionObj.c + "<br>" + 
			"<input type='radio' value='d' name='q2'> d. " + questionObj.d + "<br>";
			
		div.innerHTML = innerHtml;
	}
}
