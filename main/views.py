from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Test, Question, UserTestResult, IncorrectAnswer
from .forms import TakeTestForm


def home(request):
    tests = Test.objects.select_related('topic').all()
    return render(request, "home.html", {"tests": tests})


def test_intro(request, pk):
    test = get_object_or_404(Test, pk=pk)
    return render(request, "main/test_intro.html", {"test": test})


def take_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    questions = test.questions.prefetch_related('choices').all()

    if request.method == "POST":
        form = TakeTestForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            correct_count = 0
            total_questions = questions.count()

            if request.user.is_authenticated:
                result = UserTestResult.objects.create(
                    user=request.user,
                    test=test,
                    score=0,
                    correct_answers=0,
                    total_questions=total_questions
                )
            else:
                result = None

            for question in questions:
                chosen_choice = form.cleaned_data[f"question_{question.id}"]
                if chosen_choice.is_correct:
                    score += test.points_per_question
                    correct_count += 1
                else:
                    if result:
                        IncorrectAnswer.objects.create(
                            result=result,
                            question=question,
                            chosen_choice=chosen_choice
                        )

            if result:
                result.score = score
                result.correct_answers = correct_count
                result.save()

            messages.success(request, f"You scored {score} points!")
            return redirect("my_results" if request.user.is_authenticated else "home")
    else:
        form = TakeTestForm(questions=questions)

    return render(request, "main/take_test.html", {"test": test, "form": form})


@login_required
def my_results(request):
    results = request.user.test_results.select_related('test').order_by('-date_taken')
    return render(request, "main/my_results.html", {"results": results})


@login_required
def result_detail(request, pk):
    result = get_object_or_404(UserTestResult, pk=pk, user=request.user)
    incorrects = result.incorrect_answers.select_related('question', 'chosen_choice')

    corrects = result.test.questions.exclude(
        id__in=incorrects.values_list('question_id', flat=True)
    )

    return render(request, "main/result_detail.html", {
        "result": result,
        "incorrects": incorrects,
        "corrects": corrects,
        "incorrect_count": incorrects.count()
    })
