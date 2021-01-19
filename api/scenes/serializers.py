from rest_framework import serializers
from .models import Scene,Word,Bookmark, Understood
class SceneSerializer(serializers.ModelSerializer):
    words = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        fields = "__all__"
        model = Scene
        lookup_field = "level"
class WordSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Word
        lookup_field = "scene"
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Bookmark
class UnderstoodSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Bookmark
