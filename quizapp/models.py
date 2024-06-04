import uuid
from django.db import models
from users.models import User, Group


# Create your models here.


class Science(models.Model):
    science_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    group = models.ManyToManyField(Group, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    science = models.ForeignKey(Science, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def answers(self):
        return self.answer_set.filter(is_active=True).order_by('?')

    def __str__(self):
        return self.title


class Answer(models.Model):
    answer_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    answer = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_true = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.answer


class Result(models.Model):
    result_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    science = models.ForeignKey(Science, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    question_result = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.question_result}-{self.result_id}"


class Exam(models.Model):
    exam_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    science = models.ForeignKey(Science, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_exam = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.exam_id}-{self.user}"
