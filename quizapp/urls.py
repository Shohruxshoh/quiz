from django.urls import path
from .views import ScienceViewSet, QuestionViewSet, AnswerCreateView, QuestionByScienceAndGroupView, AnswerCheck, \
    CreateExamView, UserGetExamView, ResultUserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sciences', ScienceViewSet, basename='science')
router.register(r'questions', QuestionViewSet, basename='question')
urlpatterns = router.urls

urlpatterns += [
    path('answer/', AnswerCreateView.as_view()),
    path('exam/', UserGetExamView.as_view()),
    path('answer-check/<int:science_id>/', AnswerCheck.as_view()),
    path('exam/<int:science_id>/<int:group_id>/', CreateExamView.as_view()),
    path('test/<int:science_id>/', QuestionByScienceAndGroupView.as_view()),
    path('answer/<int:science_id>/', ResultUserView.as_view()),
]
