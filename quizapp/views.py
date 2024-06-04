from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from .serializers import ScienceSerializer, QuestionSerializer, AnswerCreateSerializer, AnswerCheckSerializer, \
    CreateExamSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Science, Question, Answer, Result, Exam
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, GenericAPIView
from users.models import Group


# Create your views here.

class ScienceViewSet(ModelViewSet):
    queryset = Science.objects.all()
    serializer_class = ScienceSerializer
    permission_classes = [IsAuthenticated]


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all().select_related("science").prefetch_related("science__group")
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


class AnswerCreateView(CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerCreateSerializer
    permission_classes = [IsAuthenticated]


class QuestionByScienceAndGroupView(GenericAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def get(self, request, science_id, group_id, *args, **kwargs):
        group = get_object_or_404(Group, id=group_id)
        questions = Question.objects.filter(science_id=science_id, science__group=group,
                                            is_active=True).select_related("science").prefetch_related(
            "science__group").order_by('?')[:30]
        serializer = QuestionSerializer(questions, many=True)
        print(serializer.data)
        return Response(serializer.data)


class AnswerCheck(GenericAPIView):
    serializer_class = AnswerCheckSerializer

    def post(self, request, science_id, group_id, *args, **kwargs):
        serializer = AnswerCheckSerializer(request.data, many=True)
        try:
            result_int = 0
            for i in serializer.data:
                question = Question.objects.filter(id=i['question_id'], answer__id=i['answer_id'], answer__is_true=True,
                                                   answer__is_active=True).exists()
                if question:
                    result_int += 1
                # answer = Answer.objects.filter(question_id=i['question_id'], is_true=True, is_active=True).first()
                # if answer.id == int(i['answer_id']):
                #     result_int += 1
                # print("i", i['question_id'])
                # print("a", i['answer_id'])
            Result.objects.create(user=request.user, science_id=science_id, group_id=group_id,
                                  question_result=result_int)

            return Response({'message': 'success'})
        except:
            return Response({'message': 'unauthorized'})


class CreateExamView(GenericAPIView):
    serializer_class = CreateExamSerializer

    def post(self, request, science_id, group_id, *args, **kwargs):
        serializer = CreateExamSerializer(request.data, many=True)
        list_exam = []
        for user in serializer.data:
            print(user)
            e = Exam(user_id=user['users_id'], science_id=science_id, group_id=group_id, is_exam=user['is_exam'])
            list_exam.append(e)

        Exam.objects.bulk_create(list_exam)

        return Response({'message': 'success'})
