from django.shortcuts import render
from django.http import JsonResponse
import random
from .models import QuizAttempt
from django.contrib.auth.decorators import login_required

# Create your views here.

def generate_question(max_digits=2):
    def weighted_random():
        num = random.randint(1, 10**max_digits - 1)
        if num % 2 == 1:
            return num
        return random.choices([num, random.randint(1, 10**max_digits - 1)], weights=[1, 2])[0]

    num1 = weighted_random()
    num2 = weighted_random()
    return num1, num2

def quiz_view(request):
    if request.method == 'GET':
        context = {
            'is_authenticated': request.user.is_authenticated
        }
        return render(request, 'quiz.html', context)
    elif request.method == 'POST':
        try:
            num1 = int(request.POST.get('num1'))
            num2 = int(request.POST.get('num2'))
            user_answer = int(request.POST.get('user_answer'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid input. Please ensure the numbers are displayed and the answer is a valid integer.'}, status=400)

        correct_answer = num1 * num2
        is_correct = (user_answer == correct_answer)

        if request.user.is_authenticated:
            # Retrieve or create a QuizAttempt instance for the user
            quiz_attempt, created = QuizAttempt.objects.get_or_create(user=request.user)

            # Update counters
            quiz_attempt.games_played += 1
            if is_correct:
                quiz_attempt.correct_submissions += 1
            else:
                quiz_attempt.incorrect_submissions += 1

            # Calculate accuracy
            if quiz_attempt.games_played > 0:
                quiz_attempt.accuracy = (quiz_attempt.correct_submissions / quiz_attempt.games_played) * 100

            # Save the updated QuizAttempt instance
            quiz_attempt.save()

        return JsonResponse({'is_correct': is_correct, 'correct_answer': correct_answer})
    return render(request, 'quiz.html')

@login_required
def generate_question_view(request):
    if request.method == 'GET':
        max_digits = int(request.GET.get('max_digits', 2))
        num1, num2 = generate_question(max_digits)
        return JsonResponse({'num1': num1, 'num2': num2})
