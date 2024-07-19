from django.shortcuts import render, get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from .models import User, Group
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .pagination import StandardResultsSetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, GroupSerializer, UserMeSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django.db.models import Q


# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().exclude(is_superuser=True)
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination
    search_fields = ['username', 'full_name', 'passpot_seriya']
    filter_backends = (filters.SearchFilter,)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination


class UserMeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserMeSerializer(user)
        return Response(serializer.data)


# GroupUserView


# Search View
@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='q', description='Search', type=str),
        ]
    )
)
class GroupUserSearchView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        group = get_object_or_404(Group, pk=pk)
        q = request.GET.get('q')
        if q and group:
            search = User.objects.filter(
                Q(username__icontains=q) | Q(full_name__icontains=q) | Q(passpot_seriya__icontains=q), group=group)
            serializer = UserMeSerializer(search, many=True)
            return Response(serializer.data)
        if not q:
            users = User.objects.filter(group=group)
            serializer = UserMeSerializer(users, many=True)
            return Response(serializer.data)
        return Response({'error': "Not found user or group"})
