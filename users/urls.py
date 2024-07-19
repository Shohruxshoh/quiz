from django.urls import path
from .views import UserViewSet, GroupViewSet, UserMeView,  GroupUserSearchView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'group', GroupViewSet, basename='group')
urlpatterns = router.urls


urlpatterns += [
    path('profile', UserMeView.as_view(), name='profile'),
    path('group-users-search/<int:pk>', GroupUserSearchView.as_view(), name='group-users-search'),
]
