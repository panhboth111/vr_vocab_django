from django.shortcuts import render
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Scene,Word,Bookmark,Understood, Percentage, PointToApprove
from .serializers import SceneSerializer,WordSerializer,BookmarkSerializer, UnderstoodSerializer, PosRotSerializer, PercentageSerializer, PercentageUpdateCompleteSerializer, PercentageUpdatePercentageSerializer, PointToApproveSerializer, UpdateUserScoreSerializer, AddUnderstoodSerializer
from .mixins import GetSerializerClassMixin
from django.contrib.auth import get_user_model
import random
# Create your views here.

User = get_user_model()
class SceneViewSet(viewsets.ModelViewSet):
    """
    list:
    get all the scenes
    retrieve:
    get all the scenes in a specific level. replace {id} with the number of level
    """
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    http_method_names = ['get','post']
    lookup_field = "level"
    def get_queryset(self):
        if 'level' in self.kwargs:
            return Scene.objects.filter(level=self.kwargs['level'])
        else:
            return Scene.objects.all()
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)
    @action(detail=False, methods=['get'], url_path="SceneNoPosRot")
    def query_scene_without_posrot(self,request):
        """
            get the scenes that contain words with position or rotation
        """
        words = Word.objects.all()
        scenes = set([word.scene for word in words if word.position == "" or word.rotation == ""])
        serializer = self.get_serializer(scenes,many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def unlock_scene(self, request):
        user = request.user
        if user.sub_plan == "Bronze":
            queried_percentage = Percentage.objects.all()
            queried_percentage_scene_names = [s.scene_name for s in queried_percentage]
            queried_scenes = Scene.objects.all().filter(~Q(scene_name__in=queried_percentage_scene_names),level=user.level)[:1]
            serializer = SceneSerializer(queried_scenes,many=True)
            return Response(serializer.data)
        if user.sub_plan == "Silver":
            queried_percentage = Percentage.objects.all()
            queried_percentage_scene_names = [s.scene_name for s in queried_percentage]
            queried_scenes = Scene.objects.all().filter(~Q(scene_name__in=queried_percentage_scene_names),level=user.level)[:2]
            serializer = SceneSerializer(queried_scenes,many=True)
            return Response(serializer.data)
        if user.sub_plan == "Gold":
            queried_scenes = Scene.objects.all().filter(level = user.level)
            serializer = SceneSerializer(queried_scenes, many=True)
            return Response(serializer.data)

class WordViewSet(GetSerializerClassMixin,viewsets.ModelViewSet):
    """
    list:
    get all words
    retrieve:
    get all words in a specific scene.
    """
    def get_queryset(self):
        if 'scene_id' in self.kwargs:
            return Word.objects.filter(scene=self.kwargs['scene_id'])
        else:
            return Word.objects.all()
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    http_method_names = ['get','post']
    serializer_action_classes = {
        'add_position_rotation':PosRotSerializer
    }
    lookup_field = "scene_id"
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)
    @action(detail=False, methods=['get'],url_path='empty/(?P<scene_id>[^/.]+)')
    def query_word_without_posrot(self,request,scene_id,pk=None):
        """
            get words that dont have position or rotation in a specific scene
        """
        words = Word.objects.all().filter(scene=scene_id).filter(Q(position = "non") |Q(rotation = "non"))
        serializer = WordSerializer(words, many = True)
        return Response(data=serializer.data)
    @action(detail=False, methods=['post'],url_path="posrot")
    def add_position_rotation(self,request):
        """ 
            add position and rotation to a word
        """
        word = Word.objects.get(id=request.data["id"])
        word.position = request.data["position"]
        word.rotation = request.data["rotation"]
        word.save()
        serializer = WordSerializer(word)
        return Response(serializer.data)
class BookmarkViewSet(viewsets.ModelViewSet):
    """
        list:
        (token) get all bookmarks of a specific user
        retrieve:
        create:
        (token) add bookmark for a user
        delete:
        (token) unbookmark
    """
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','delete']
    def list(self, request):
        user = request.user
        bookmarks = Bookmark.objects.all().filter(user=user.id) 
        serializer = BookmarkSerializer(bookmarks,many=True)
        return Response(serializer.data)
    def create(self,request):
        user = request.user
        bookmark = Bookmark(user=user,word=request.data["word"],definition=request.data["definition"])
        bookmark.save()
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data)
class RecommendationViewSet(viewsets.ModelViewSet):
    """
        list:
        (token) list down the recommended scenes for a user
    """
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    def list(self, request):
        user = request.user
        recommendation = Scene.objects.all().filter(level=user.level)
        serializer = SceneSerializer(recommendation, many=True)
        return Response(serializer.data)
class UnderstoodViewSet(GetSerializerClassMixin,viewsets.ModelViewSet):
    """
        list:
        (token) get all the understood words of a specific user
        retrieve:
        create:
        (token) add an understood word for a user
    """
    queryset = Understood.objects.all()
    serializer_class = UnderstoodSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post']
    serializer_action_classes = {
        'create':AddUnderstoodSerializer
    }
    def list(self, request):
        user = request.user
        understood = Understood.objects.all().filter(user=user.id)
        serializer = UnderstoodSerializer(understood, many = True)
        return Response(serializer.data)
    def create(self, request):
        user = request.user
        serializer = AddUnderstoodSerializer(data = request.data)
        if serializer.is_valid():
            understood = Understood(word=serializer.data.get("word"),user=user)
            understood.save()
            point = PointToApprove.objects.filter(user = user)
            if point.exists():
                point = PointToApprove.objects.get(user = user)
                point.target_point += serializer.data.get("target_point")
                point.save()
            else:
                create_point_to_approve = PointToApprove(target_point = serializer.data.get("target_point"), user=user)
                create_point_to_approve.save()
            serializer = UnderstoodSerializer(understood)
            return Response(serializer.data)
        return Response(serializer.errors)
class PercentageViewSet(GetSerializerClassMixin,viewsets.ModelViewSet):
    """
    create:
    (token)create percentage for a user
    list:
    (token)get all percentage in all scenes for a user
    update_percentage:
    (token)update percentage in a specific scene for a user
    update_complete:
    (token)update complete in a specific scene for a user
    """
    queryset = Percentage.objects.all()
    serializer_class = PercentageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post']
    serializer_action_classes = {
        'update_percentage':PercentageUpdatePercentageSerializer,
        'update_complete':PercentageUpdateCompleteSerializer
    }
    def create(self,request):
        user = request.user
        queried_percentage = Percentage.objects.all().filter(user=user.id,scene_name=request.data["scene_name"])
        if len(queried_percentage) > 0:
            return Response("The percentage for this user in this scene has already been created")
        new_percentage = Percentage(scene_name=request.data["scene_name"],user=user,percentage=request.data["percentage"], total_vocab=request.data["total_vocab"], complete=request.data["complete"])
        new_percentage.save()
        serializer = self.get_serializer(new_percentage)
        return Response(serializer.data)
    def list(self,request):
        user = request.user
        percentage = Percentage.objects.all().filter(user=user.id)
        serializer = self.get_serializer(percentage, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['post'])
    def update_percentage(self,request):
        user = request.user
        percentage = Percentage.objects.get(user=user.id,scene_name=request.data["scene_name"])
        percentage.percentage = request.data["percentage"]
        percentage.save()
        return Response("percentage updated successfully")
    @action(detail=False, methods=['post'])
    def update_complete(self,request):
        user = request.user
        percentage = Percentage.objects.get(user=user.id,scene_name=request.data["scene_name"])
        percentage.complete = request.data["complete"]
        percentage.save()
        return Response("complete updated successfully")
class PointToApproveViewSet(GetSerializerClassMixin,viewsets.ModelViewSet):
    queryset = PointToApprove.objects.all()
    serializer_class = PointToApproveSerializer
    permission_classes = [IsAuthenticated]
    serializer_action_classes = {
        'update_score': UpdateUserScoreSerializer
    }
    def list(self, request):
        user = request.user
        point = PointToApprove.objects.all()
        serializer = PointToApproveSerializer(point, many = True)
        return Response(serializer.data)
    @action(detail=False, methods=['post'])
    def update_score(self, request):
        user = request.user
        serializer = UpdateUserScoreSerializer(data = request.data)
        if serializer.is_valid():
            queried_user = User.objects.get(id=user.id)
            queried_point = PointToApprove.objects.get(user = user.id)
            final_score = (queried_point.target_point * serializer.data.get("percentage"))/100
            queried_user.score += final_score
            queried_user.save()
            queried_user.coin += serializer.data.get("coin")
            queried_user.save()
            queried_point.target_point = 0
            queried_point.save()
            return Response("Score and Coin updated successfully")
        return Response(serializer.errors)
