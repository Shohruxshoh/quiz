from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from users.pagination import StandardResultsSetPagination
from .serializers import ScienceSerializer, QuestionSerializer, AnswerCreateSerializer, AnswerCheckSerializer, \
    CreateExamSerializer, ExamSerializer, ResultUserSerializer, ResultSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Science, Question, Answer, Result, Exam
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from users.models import Group


# Create your views here.

class ScienceViewSet(ModelViewSet):
    queryset = Science.objects.all()
    serializer_class = ScienceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


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

    permission_classes = [IsAuthenticated]

    def get(self, request, science_id, *args, **kwargs):
        group = get_object_or_404(Group, id=request.user.group.id)
        questions = Question.objects.filter(science_id=science_id, science__group=group,
                                            is_active=True).select_related("science").prefetch_related(
            "science__group").order_by('?')[:30]
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class AnswerCheck(GenericAPIView):
    serializer_class = AnswerCheckSerializer

    permission_classes = [IsAuthenticated]

    def post(self, request, science_id, *args, **kwargs):
        serializer = AnswerCheckSerializer(request.data, many=True)
        try:
            # result_int = 0
            # for i in serializer.data:
            #     question = Question.objects.filter(id=int(i['question_id']), answer__id=int(i['answer_id']),
            #                                        answer__is_true=True, answer__is_active=True).exists()
            #     if question:
            #         result_int += 1
            # answer = Answer.objects.filter(question_id=i['question_id'], is_true=True, is_active=True).first()
            # if answer.id == int(i['answer_id']):
            #     result_int += 1
            # print("i", i['question_id'])
            # print("a", i['answer_id'])
            question_ids = [int(i['question_id']) for i in serializer.data]
            answer_ids = [int(i['answer_id']) for i in serializer.data]

            correct_answers = Question.objects.filter(
                id__in=question_ids,
                answer__id__in=answer_ids,
                answer__is_true=True,
                answer__is_active=True
            ).select_related('answer').values_list('id', flat=True)

            result_int = len(correct_answers)
            r = Result.objects.filter(user=request.user, science_id=science_id, group_id=request.user.group.id,
                                      is_active=True).select_related("science", 'group', 'user').last()
            if r:
                r.is_active = False
                r.save()

            Result.objects.create(user=request.user, science_id=science_id, group_id=request.user.group.id,
                                  question_result=result_int)
            exam = Exam.objects.filter(user_id=request.user.id, science_id=science_id, group_id=request.user.group.id,
                                       is_exam=True, is_active=True).select_related("science", 'group', 'user').last()
            if exam:
                exam.is_exam = False
                exam.save()

            return Response({'message': 'success'})
        except Exception as e:
            print(e)
            return Response({'message': 'unauthorized'})


class CreateExamView(GenericAPIView):
    serializer_class = CreateExamSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, science_id, group_id, *args, **kwargs):
        serializer = CreateExamSerializer(request.data, many=True)
        list_exam = []
        for user in serializer.data:
            if not Exam.objects.filter(user_id=user['users_id'], science_id=science_id, group_id=group_id, is_exam=True,
                                       is_active=True).select_related("science", 'group').exists():
                e = Exam(user_id=user['users_id'], science_id=science_id, group_id=group_id, is_exam=user['is_exam'])
                list_exam.append(e)

        Exam.objects.bulk_create(list_exam)

        return Response({'message': 'success'})


class UserGetExamView(GenericAPIView):
    serializer_class = ExamSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        exam = Exam.objects.filter(user=request.user, is_active=True)
        serializer = ExamSerializer(exam, many=True)
        return Response(serializer.data)


class ResultUserView(GenericAPIView):
    serializer_class = ResultUserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, science_id, *args, **kwargs):
        result = get_object_or_404(Result, science_id=science_id, user=request.user, group=request.user.group,
                                   is_active=True)
        serializer = ResultUserSerializer(result)
        return Response(serializer.data)


class ResultListView(ListAPIView):
    queryset = Result.objects.filter(is_active=True)
    serializer_class = ResultSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination


class ExamViewList(ListAPIView):
    queryset = Exam.objects.filter(is_active=True)
    serializer_class = ExamSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

