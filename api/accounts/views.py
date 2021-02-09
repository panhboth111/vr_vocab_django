from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, action
from .serializers import UserSerializer, ChangePasswordSerializer, UpdateUserLevelSerializer, UpdateUserScoreSerializer, TemporaryForgotPasswordSerializer, ConfirmedCodeSerializer, ForgotPasswordSerializer, SendEmailSerializer
from .models import ForgotPassword, CustomUser
from rest_framework.generics import UpdateAPIView
from .mixins import GetSerializerClassMixin


User = get_user_model()
class UserViewSet(GetSerializerClassMixin,viewsets.ModelViewSet):
    """
    create:
    register a new account
    get_user_info:
    (token)get the information of a specific user
    change_password:
    (token)change user's password
    update_score:
    (token)add the score from correct answer in quiz to the user's current score
    update_level:
    (token) update the user's level
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_action_classes = {
        'change_password': ChangePasswordSerializer,
        'update_level':UpdateUserLevelSerializer,
        'update_score': UpdateUserScoreSerializer,
        'send_email': SendEmailSerializer,
        'confirmed_code': ConfirmedCodeSerializer,
        'forgot_password': ForgotPasswordSerializer
    }
    http_method_names = ['post','get']
    
    @action(detail=False, methods=['get'],url_path="info",permission_classes=[IsAuthenticated])
    def get_user_info(self,request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    def list(self,request):
        return Response("you are not authorized to access this route")
    def retrieve(self,request, pk=None):
        return Response("you are not authorized to access this route")

    @action(detail=False, methods=['post'],permission_classes=[IsAuthenticated])
    def change_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Incorrect password."]})
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response("Password changed successfully")
        return Response(serializer.errors)

    @action(detail=False, methods=['post'])
    def send_email(self, request):
        serializer = SendEmailSerializer(data = request.data)
        if serializer.is_valid():
            verify = get_random_string(length=6, allowed_chars='1234567890')
            email = User.objects.filter(email = serializer.data.get("email"))
            if email.exists():
                subject = "Password Reset Requested"
                message = "Here your verification code:"
                send_mail(subject, message+"\n"+verify, 'lenofreality@kit.edu.kh', email, fail_silently = False)
                forgot_password = ForgotPassword(email = serializer.data.get("email"), code = verify)
                forgot_password.save()
                serializer = TemporaryForgotPasswordSerializer(forgot_password)
                return Response(serializer.data)
            return Response("Invalid Email")
        return Response(serializer.errors)

    @action(detail=False, methods=['post'])
    def confirmed_code(self, request):
        serializer = ConfirmedCodeSerializer(data = request.data)
        if serializer.is_valid():
            check = ForgotPassword.objects.all().filter(code = serializer.data.get("code"), id = serializer.data.get("id"))
            if len(check) > 0:
                forgot_password = ForgotPassword.objects.get(id = serializer.data.get("id"))
                forgot_password.confirmed = True
                forgot_password.save()
                return Response("Code confirmed")
            return Response("Invalid Code")
        return Response(serializer.errors)

    @action(detail=False, methods=['post'])
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data = request.data)
        if serializer.is_valid():
            forgot_password = ForgotPassword.objects.get(id = serializer.data.get("id"))
            if forgot_password.confirmed == True:
                user = CustomUser.objects.get(email = forgot_password.email)
                user.set_password(serializer.data.get("new_password"))
                user.save()
                forgot_password.delete()
                return Response("Reset password successful")
            return Response("Verification code didn't confirm yet!")
        return Response(serializer.errors)

    @action(detail=False, methods=['post'],permission_classes=[IsAuthenticated])
    def update_score(self,request):
        serializer = UpdateUserScoreSerializer
        user = request.user
        queried_user = User.objects.get(email=user.email)
        queried_user.score = queried_user.score + request.data["score"]
        queried_user.save()
        return Response("user score updated successfully")
    @action(detail=False, methods=['post'],permission_classes=[IsAuthenticated])
    def update_level(self,request):
        serializer = UpdateUserLevelSerializer
        user = request.user
        queried_user = User.objects.get(email=user.email)
        queried_user.level = request.data["level"]
        queried_user.save()
        return Response("user level updated successfully")
            
