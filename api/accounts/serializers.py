from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from .models import ForgotPassword, Card
import datetime


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    is_active = serializers.BooleanField()
    class Meta:
        model = User
        fields = ('id','username', 'password', 'email','is_active', 'sub_plan')

    def validate(self, attrs):
        if not attrs['is_active']:
            raise serializers.ValidationError({"active": "Account's email needs to be confirmed"})
        return attrs
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class SendEmailSerializer(serializers.Serializer):
    model = User
    email = serializers.CharField(required=True)

class TemporaryForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = ForgotPassword

class ConfirmedCodeSerializer(serializers.Serializer):
    model = ForgotPassword
    code = serializers.IntegerField(required=True)
    id = serializers.IntegerField(required=True)

class ForgotPasswordSerializer(serializers.Serializer):
    model = User
    id = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True)

class UpdateUserScoreSerializer(serializers.Serializer):
    model = User
    score = serializers.IntegerField(required=True)

class UpdateUserLevelSerializer(serializers.Serializer):
    model = User
    level = serializers.IntegerField(required=True)

class TopScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'score')

class CardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Card
		fields = '__all__'

class UpdateUserPlanSerializer(serializers.Serializer):
    model = User
    sub_plan = serializers.CharField(required=True)