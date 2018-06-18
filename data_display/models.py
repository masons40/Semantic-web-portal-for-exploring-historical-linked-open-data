from django.db import models

class Type(models.Model):
    type = models.CharField(max_length=250)

class Questionnaire(models.Model):
    Questionnaire_id = models.IntegerField(primary_key=True)
    Questionnaire_type = models.ForeignKey(Type,on_delete=models.CASCADE)
    Questionnaire_label = models.CharField(max_length=250)
    Questionnaire_note = models.CharField(max_length=250)
    Questionnaire_title = models.CharField(max_length=250)
    Questionnaire_publication_year = models.PositiveSmallIntegerField(blank=True, null=True)
	
	
    def display_id(self):
	    return self.Questionnaire_id
	
    def display_type(self):
	    return self.Questionnaire_type

    def display_label(self):
        return self.Questionnaire_label

    def display_note(self):
        return self.Questionnaire_note
		
    def display_title(self):
        return self.Questionnaire_title
		
    def display_publication_year(self):
        return self.Questionnaire_publication_year
		
		
class Question(models.Model):
    Question_id = models.ForeignKey(Questionnaire,on_delete=models.CASCADE)
    Question_type = models.ForeignKey(Type,on_delete=models.CASCADE)
    Is_question_of = models.IntegerField()
    Question_number = models.CharField(primary_key=True, max_length=50)
    Original_question = models.CharField(max_length=250)
    Short_question = models.CharField(max_length=250)
	
	
    def display_question_id(self):
	    return self.Question_id
	
    def display_question_type(self):
	    return self.Question_type

    def display_is_question_of(self):
        return self.Is_Question_of

    def display_question_number(self):
        return self.Question_number
		
    def display_original_question(self):
        return self.Original_Question
		
    def display_short_question(self):
        return self.Short_Question
	

	
