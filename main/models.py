from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Test(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="tests")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes")
    points_per_question = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} ({self.topic})"

    def question_count(self):
        return self.questions.count()


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_results")
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.test} ({self.score})"


class IncorrectAnswer(models.Model):
    result = models.ForeignKey(UserTestResult, on_delete=models.CASCADE, related_name="incorrect_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.result.user} - {self.question}"
