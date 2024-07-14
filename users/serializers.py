from rest_framework import serializers
from .models import User, Group


class UserSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')

    class Meta:
        model = User
        fields = ['id', 'username', 'user_id', 'full_name', "group", 'passpot_seriya']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data["username"], password=validated_data["passpot_seriya"],
                                   full_name=validated_data["full_name"], group=validated_data["group"],
                                   passpot_seriya=validated_data["passpot_seriya"])
        user.set_password(validated_data["passpot_seriya"])
        user.save()
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "group_id", "name"]


class UserMeSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')

    class Meta:
        model = User
        fields = ['id', 'username', 'user_id', 'full_name', 'passpot_seriya', 'group']
