SELECT * FROM may1713_PrisonGardenApp.Quiz_Answers;

INSERT into Bed_Plans (Bed_Name, Bed_Plan) 
		values ("Venus", "SADASDSDADSDSadsdadas")

SELECT QA.Username, QQ.Question_Text, QAn.Answer_Text 
from Quiz_Questions QQ, Quiz_Attempts QA, Quiz_Answers QAn 
where (QQ.QuestionID = QA.Question1_ID and QAn.AnswerID = QA.Answer1_ID 
						or QQ.QuestionID = QA.Question2_ID and QAn.AnswerID = QA.Answer2_ID 
                        or QQ.QuestionID = QA.Question3_ID and QAn.AnswerID = QA.Answer3_ID    
                        or QQ.QuestionID = QA.Question4_ID and QAn.AnswerID = QA.Answer4_ID    
                        or QQ.QuestionID = QA.Question5_ID and QAn.AnswerID = QA.Answer5_ID    
                        or QQ.QuestionID = QA.Question6_ID and QAn.AnswerID = QA.Answer6_ID    
                        or QQ.QuestionID = QA.Question7_ID and QAn.AnswerID = QA.Answer7_ID    
                        or QQ.QuestionID = QA.Question8_ID and QAn.AnswerID = QA.Answer8_ID    
                        or QQ.QuestionID = QA.Question9_ID and QAn.AnswerID = QA.Answer9_ID    
                        or QQ.QuestionID = QA.Question10_ID and QAn.AnswerID = QA.Answer10_ID);
                        
SELECT QA.ID, QA.Username as user, QA.Course_Name as course, C.Course_Order as chapter, QA.Passed 
FROM Quiz_Attempts QA, Courses C 
WHERE C.Course_Name = QA.Course_Name 
AND QA.ID in (SELECT MAX(ID) 
				FROM Quiz_Attempts 
                where Username = QA.Username 
                and Course_Name = QA.Course_Name) 
ORDER BY QA.Username, C.Course_Order;