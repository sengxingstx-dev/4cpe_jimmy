from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from .models import QuizProfile, Question, AttemptedQuestion
from .forms import UserLoginForm, RegistrationForm
from . import models
from . import forms


def home(request):
    context = {}
    return render(request, 'quiz/home.html', context=context)


@login_required()
def user_home(request):
    context = {}
    return render(request, 'quiz/user_home.html', context=context)


def leaderboard(request):

    top_quiz_profiles = QuizProfile.objects.order_by('-total_score')[:500]
    total_count = top_quiz_profiles.count()
    context = {
        'top_quiz_profiles': top_quiz_profiles,
        'total_count': total_count,
    }
    return render(request, 'quiz/leaderboard.html', context=context)


@login_required()
def play(request):
    quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        question_pk = request.POST.get('question_pk')

        attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=question_pk)

        choice_pk = request.POST.get('choice_pk')

        try:
            selected_choice = attempted_question.question.choices.get(pk=choice_pk)
        except ObjectDoesNotExist:
            raise Http404

        quiz_profile.evaluate_attempt(attempted_question, selected_choice)

        return redirect(attempted_question)

    else:
        question = quiz_profile.get_new_question()
        if question is not None:
            quiz_profile.create_attempt(question)

        context = {
            'question': question,
        }

        return render(request, 'quiz/play.html', context=context)


@login_required()
def submission_result(request, attempted_question_pk):
    attempted_question = get_object_or_404(AttemptedQuestion, pk=attempted_question_pk)
    context = {
        'attempted_question': attempted_question,
    }

    return render(request, 'quiz/submission_result.html', context=context)


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('quiz:home')
    return render(request, 'quiz/login.html', {"form": form, "title": title})


def register(request):
    title = "Create account"
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegistrationForm()

    context = {'form': form, 'title': title}
    return render(request, 'quiz/registration.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/')


def error_404(request):
    data = {}
    return render(request, 'quiz/error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'quiz/error_500.html', data)


def create_class_room_view(request):
    if request.method == 'POST':
        form = forms.ClassRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz:home')
    else:
        form = forms.ClassRoomForm()
        print(form.errors)
        # form = UserProfileForm(instance=request.user)
    
    return render(request, 'quiz/classroom.html', {'form': form})


def update_class_room_view(request, pk):
    classroom = models.ClassRoom.objects.get(id=pk)

    if request.method == 'POST':
        form = forms.ClassRoomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=pk)
    else:
        form = forms.ClassRoomForm(instance=classroom)
        print(form.errors)
        # form = UserProfileForm(instance=request.user)
    
    return render(request, 'quiz/classroom.html', {'form': form})


# def create_question_view(request):
#     if request.method == 'POST':
#         form = forms.QuestionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('quiz:home')
#     else:
#         form = forms.QuestionForm()
#         print(form.errors)
#         # form = UserProfileForm(instance=request.user)
    
#     return render(request, 'quiz/create_questions.html', {'form': form})

def create_question_view(request):
    if request.method == 'POST':
        form = forms.QuestionForm(request.POST)
        choice_formset = forms.ChoiceInlineFormset(request.POST, prefix='choice_formset')
        if form.is_valid() and choice_formset.is_valid():
            question = form.save()
            choice_formset.instance = question
            choice_formset.save()
            # Handle successful form submission, e.g., redirect or render success message
    else:
        form = forms.QuestionForm()
        choice_formset = forms.ChoiceInlineFormset(prefix='choice_formset')

    return render(request, 'quiz/create_questions.html', {'form': form, 'choice_formset': choice_formset})
