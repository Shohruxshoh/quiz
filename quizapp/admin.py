from django.contrib import admin
from .models import Answer, Question, Science, Result, Exam

# Register your models here.

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Science)
admin.site.register(Result)
admin.site.register(Exam)
