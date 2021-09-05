from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CorrectionWord(models.Model):
    incorrect_word = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Extrainfo(models.Model):
    grade_level = models.CharField(max_length=2)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
