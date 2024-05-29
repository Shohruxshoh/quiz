from django.shortcuts import render
from .models import User, Group
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer, GroupSerializer
from rest_framework.viewsets import ModelViewSet


# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

