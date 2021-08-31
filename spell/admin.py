from django.contrib import admin
from .models import Extrainfo, NewWord, CorrectionWord
# Register your models here.
admin.site.register(Extrainfo)
admin.site.register(NewWord)
admin.site.register(CorrectionWord)