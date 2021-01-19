from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, action
from .serializers import UserSerializer



User = get_user_model()
class UserViewSet(viewsets.ModelViewSet):
    """
    create:
    register a new account
    get_user_info:
    get the information of a specific user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post','get']
    
    @action(detail=False, methods=['get'],url_path="info",permission_classes=[IsAuthenticated])
    def get_user_info(self,request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
