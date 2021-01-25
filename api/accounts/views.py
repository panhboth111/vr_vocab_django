from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, action
from .serializers import UserSerializer, ChangePasswordSerializer, UpdateUserLevelSerializer, UpdateUserScoreSerializer
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
        'update_score': UpdateUserScoreSerializer
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
    @action(detail=False, methods=['post'],permission_classes=[IsAuthenticated])
    def update_score(self,request):
        serializer = UpdateUserScoreSerializer
        user = request.user
        queried_user = User.objects.all(email=user.email)
        queried_user.score = queried_user.score + request.data["additional_score"]
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
    # @action(detail=False, methods=['post'],permission_classes=[IsAuthenticated])
    # def forgot_password(self, request):
    #     user = request.user
    #     serializer = ForgotPasswordSerializer(data=request.data)
    #     if serializer.is_valid():
            
