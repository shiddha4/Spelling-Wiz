from django.shortcuts import render, redirect
import random
# Create your views here.
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Extrainfo, CorrectionWord
import random
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#gets random word - input : grade, output:word matching grade
def random_word(grade):
    if int(grade) < 10:
        word_list = []
        words = open('words/words.txt', 'r')
        con_grade_level = str(grade)
        for word in words:
            for letter in word:
                if grade in letter:
                    word_list.append(word.replace(f',{con_grade_level}', ''))
        word=random.choice(word_list).strip()
        return word


def correct(request):
    try:
        word = request.POST.get('user_word').lower().strip()
        correct_word = request.POST.get('word').lower().strip()
        if word == correct_word:
            data = {'msg': 'This is correct',
                    "correct": True}
            return JsonResponse(data)
        else:
            current_user = request.user
            if CorrectionWord.objects.filter(user=current_user.id, incorrect_word=correct_word):
                pass
            else:
                incorrect_word = CorrectionWord(user=request.user, incorrect_word=correct_word)
                incorrect_word.save()
            data = {'msg': 'This incorrect',
                    'not_correct': True}
            return JsonResponse(data)
    except:
        return redirect('/quiz/')


def home(request):
    return render(request, 'home.html', {'User': request.user})


@login_required(login_url='/login/')
def quiz(request):
    return render(request,'quiz.html', {'word': random_word(str(request.user.extrainfo.grade_level))})


def verify(request):
    if request.method == 'POST':
        first_name = request.POST['First Name']
        last_name = request.POST['Last Name']
        username = request.POST['username']
        password_1 = request.POST['psw']
        password_2 = request.POST['psw2']
        email = request.POST['Email']
        user_grade_level = request.POST['grade_level']
        if password_1 != password_2:
            messages.error(request,'Passwords do not match')
            return redirect('/create/')
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('/create/')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email taken')
            return redirect('/create/')
        user = User.objects.create_user(username=username, password=password_1, first_name=first_name, last_name=last_name, email=email)
        user.save()
        authentication = authenticate(username=username, password=password_1)
        auth.login(request, authentication)
        extra_info_about_user = Extrainfo(grade_level=user_grade_level,user=request.user)
        extra_info_about_user.save()
        return redirect('/')
    else:
        return render(request, 'create_user.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
           messages.error(request, 'Invalid credentials')
           return redirect('/login/')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def settings(request):
    return render(request, 'settings.html', {'User': request.user})


@login_required(login_url='/login/')
def grade(request):
    if request.method == 'POST':
        grade = request.POST['grade_level']
        user_info = Extrainfo.objects.get(user=request.user.id)
        user_info.grade_level = grade
        user_info.save()
        messages.success(request, 'Profile details updated.')
        return redirect('/settings/')
    else:
        return redirect('/settings/')


@login_required(login_url='/login/')
def study(request):
    current_user = request.user
    return render(request, 'study.html', {'words': CorrectionWord.objects.filter(user=current_user.id)})


