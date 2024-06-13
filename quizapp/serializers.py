from rest_framework import serializers
from users.serializers import GroupSerializer
from quizapp.models import Science, Question, Answer, Exam


class ScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = ['id', 'science_id', 'is_active', 'name', 'group']


class ScienceNotGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = ['id', 'science_id', 'is_active', 'name']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_id', 'answer', 'is_active', "question"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(read_only=True, many=True)
    science = ScienceNotGroupSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_id', 'title', 'is_active', 'science', 'answers']


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answer', 'is_active', "question", "is_true"]


class AnswerCheckSerializer(serializers.Serializer):
    question_id = serializers.CharField(max_length=200)
    answer_id = serializers.CharField(max_length=200)


class CreateExamSerializer(serializers.Serializer):
    users_id = serializers.CharField(max_length=200)
    is_exam = serializers.BooleanField(default=False)


class ExamSerializer(serializers.ModelSerializer):
    science = ScienceNotGroupSerializer(read_only=True)
    class Meta:
        model = Exam
        fields = ['id', 'exam_id', 'user', 'science', 'group', 'is_active', 'is_exam']
