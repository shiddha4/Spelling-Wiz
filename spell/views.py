from django.shortcuts import render,redirect
import random
# Create your views here.
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Extrainfo
import random
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


def random_word(grade):
    if int(grade)<10:
        word_list = []
        words = open('words/words.txt', 'r')
        con_grade_level=str(grade)
        for word in words:
            for letter in word:
                if grade in letter:
                     word_list.append(word.replace(f',{con_grade_level}',''))
        word=random.choice(word_list).strip()
        return word
    else:
        pass
        # if grade == 12:
        #     word_list = []
        #     words = open('words/12.txt', 'r')
        #     con_grade_level = str(grade)
        #     for word in words:
        #         for letter in word:
        #             if grade in letter:
        #                 word_list.append(word.replace(f',{con_grade_level}', ''))
        #     word = random.choice(word_list).strip()
        #     return word
        # elif grade == 11:
        #     words = open('words/12.txt', 'r')
        #     con_grade_level = str(grade)
        #     for word in words:
        #         for letter in word:
        #             if grade in letter:
        #                 word_list.append(word.replace(f',{con_grade_level}', ''))
        #     word = random.choice(word_list).strip()
        #     return word
        # elif grade == '10':
        #     words = open('words/10.txt', 'r')
        #     con_grade_level = str(grade)
        #     for word in words:
        #         for letter in word:
        #             if grade in letter:
        #                 word_list.append(word.replace(f',{con_grade_level}', ''))
        #     word = random.choice(word_list).strip()
        #     return word
        #
        # else:
        #     pass
        #





def correct(request):
    if request.is_ajax:
        word = request.POST.get('user_word').lower().strip()
        correct_word=request.POST.get('word').lower().strip()
        if word==correct_word:
            data = {'msg': 'This is correct',
                    "correct":True}
            return JsonResponse(data)
        else:
            data = {'msg': 'This incorrect',
                    'correct':False}
            return JsonResponse(data)
    else:
        return redirect('/')









def home(request):
    return render(request, 'home.html',{'User':request.user})






@login_required(login_url='/login/')
def quiz(request):
    return render(request,'quiz.html', {'word': random_word(str(request.user.extrainfo.grade_level))})




def verfy(request):
    if request.method == 'POST':
        first_name=request.POST['First Name']
        last_name=request.POST['Last Name']
        username=request.POST['usrname']
        password_1=request.POST['psw']
        password_2=request.POST['psw2']
        email=request.POST['Email']
        user_grade_level=request.POST['grade_level']
        if password_1!=password_2:
            return render(request,'create_user.html',{'error':True,'msg':'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'create_user.html', {'error': True, 'msg': 'Username taken'})
        user=User.objects.create_user(username=username,password=password_1,first_name=first_name,last_name=last_name,email=email)
        user.save()
        userszs = authenticate(username=username, password=password_1)
        auth.login(request,userszs)
        extrainfo=Extrainfo(grade_level=user_grade_level,user=request.user)
        extrainfo.save()
        return redirect('/')
    else:
        return render(request,'create_user.html')



def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            return render(request,'login.html',{'error_message':True,'username':username,'password':password})

    else:
        return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')



@login_required(login_url='/login/')
def settings(request):
    grade=''
    if User.last_name=='1':
        grade="st grade"
    elif User.last_name=='2':
        grade="nd grade"
    elif User.last_name == '3':
        grade = "rd grade"
    elif  User.last_name=='4' or '5' or '6' or '7' or '8' or '9':
        grade='th grade'
    return render(request,'settings.html',{"User_grade":grade,
                                           'User':request.user})