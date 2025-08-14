import nested_admin
from django.contrib import admin
from .models import Topic, Test, Question, Choice, UserTestResult, IncorrectAnswer


class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 4
    min_num = 0
    max_num = 6


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]


@admin.register(Test)
class TestAdmin(nested_admin.NestedModelAdmin):
    list_display = ("title", "topic", "time_limit", "points_per_question", "question_count")
    list_filter = ("topic",)
    search_fields = ("title",)
    inlines = [QuestionInline]  # Shows Questions inline under Test


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(UserTestResult)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("user", "test", "score", "correct_answers", "total_questions", "date_taken")
    list_filter = ("test", "date_taken")
    search_fields = ("user__username", "test__title")


@admin.register(IncorrectAnswer)
class IncorrectAnswerAdmin(admin.ModelAdmin):
    list_display = ("result", "question", "chosen_choice")
    search_fields = ("question__text",)
