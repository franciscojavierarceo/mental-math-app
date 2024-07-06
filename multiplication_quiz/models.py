from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num1 = models.IntegerField()
    num2 = models.IntegerField()
    user_answer = models.IntegerField()
    correct_answer = models.IntegerField()
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    games_played = models.IntegerField(default=0)
    correct_submissions = models.IntegerField(default=0)
    incorrect_submissions = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.num1} x {self.num2} = {self.user_answer} ({'Correct' if self.is_correct else 'Incorrect'})"
