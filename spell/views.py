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
    words = open('words/words.txt', 'r')
    word_list = []
    con_grade_level=str(grade)
    for word in words:
        for letter in word:
            if grade in letter:
                 word_list.append(word.replace(f',{con_grade_level}',''))
    word=random.choice(word_list).strip()
    return word




def correct(request):
    if request.is_ajax:
        word = request.POST.get('user_word').lower().strip()
        correct_word=request.POST.get('word').lower().strip()
        if word==correct_word:
            data = {'msg': 'This is correct'}
            return JsonResponse(data)
        else:
            data = {'msg': 'This incorrect'}
            return JsonResponse(data)
    else:
        return redirect('/')







def home(request):
    print(User.first_name)
    return render(request, 'home.html',{'User':request.user})



@login_required(login_url='/login/')
def quiz(request):
    return render(request,'quiz.html', {'word': random_word(str(5))})




def verfy(request):
    if request.method=='POST':
        first_name=request.POST['First Name']
        last_name=request.POST['Last Name']
        username=request.POST['usrname']
        password_1=request.POST['psw']
        password_2=request.POST['psw2']
        user_grade_level=request.POST['grade_level']
        if password_1!=password_2:
            return render(request,'create_user.html',{'error':True,'msg':'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'create_user.html', {'error': True, 'msg': 'Username taken'})
        user=User.objects.create_user(username=username,password=password_1,first_name=first_name,last_name=last_name)
        print(user)
        user.save()
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
