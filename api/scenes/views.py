from django.shortcuts import render
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Scene,Word,Bookmark,Understood
from .serializers import SceneSerializer,WordSerializer,BookmarkSerializer,UnderstoodSerializer
# Create your views here.

class SceneViewSet(viewsets.ModelViewSet):
    """
    list:
    get all the scenes
    retrieve:
    get all the scenes in a specific level. replace {id} with the number of level
    """
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    http_method_names = ['get']
    lookup_field = "level"
    def get_queryset(self):
        if 'level' in self.kwargs:
            return Scene.objects.filter(level=self.kwargs['level'])
        else:
            return Scene.objects.all()
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)
    @action(detail=False, methods=['get'])
    def query_scene_without_posrot(self,request):
        """
            get the scenes that contain words with position or rotation
        """
        words = Word.objects.all()
        scenes = [word.scene for word in words if word.position == "" or word.rotation == ""]
        serializer = self.get_serializer(scenes,many=True)
        return Response(serializer.data)

class WordViewSet(viewsets.ModelViewSet):
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
    lookup_field = "scene_id"
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)
    @action(detail=False, methods=['get'],url_path='empty/(?P<scene_id>[^/.]+)')
    def query_word_without_posrot(self,request,scene_id,pk=None):
        """
            get words that dont have position or rotation in a specific scene
        """
        words = Word.objects.all().filter(scene=scene_id).filter(Q(position = "") |Q(rotation = ""))
        serializer = WordSerializer(words, many = True)
        return Response(data=serializer.data)
    @action(detail=False, methods=['post'],url_path="posrot")
    def add_position_rotation(self,request):
        """ 
            add position and rotation to a word
        """
        word = Word.objects.get(word=request.data["word"])
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
class UnderstoodViewSet(viewsets.ModelViewSet):
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
    def list(self, request):
        user = request.user
        understood = Understood.objects.all().filter(user=user.id)
        serializer = UnderstoodSerializer(understood, many = True)
        return Response(serializer.data)
    def create(self, request):
        user = request.user
        understood = Understood(word=request.data["word"],user=user)
        understood.save()
        serializer = UnderstoodSerializer(understood)
        return Response(serializer.data)