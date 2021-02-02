from rest_framework import serializers
from .models import Scene,Word,Bookmark, Understood, Percentage
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
        extra_kwargs = {'synonym': {'required': False}, 'position': {'required': False},'rotation': {'required': False}} 
        lookup_field = "scene"
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Bookmark
class UnderstoodSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Understood
class PosRotSerializer(serializers.Serializer):
    model = Word
    id = serializers.IntegerField(required=True)
    position = serializers.CharField(required=True)
    rotation = serializers.CharField(required=True)


class PercentageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["scene_name","percentage","total_vocab","complete"]
        model = Percentage

class PercentageUpdatePercentageSerializer(serializers.Serializer):
    scene_name = serializers.CharField(required=True)
    percentage = serializers.CharField(required=True)

class PercentageUpdateCompleteSerializer(serializers.Serializer):
    scene_name = serializers.CharField(required=True)
    complete = serializers.CharField(required=True)
