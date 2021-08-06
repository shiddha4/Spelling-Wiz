from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('correct/',views.correct,name='correct'),
    path('quiz/',views.quiz,name='quiz'),
    path('create/', views.verfy, name='verfy'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout')

]