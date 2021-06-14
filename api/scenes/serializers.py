from rest_framework import serializers
from .models import Scene,Word,Bookmark, Understood, Percentage, PointToApprove , Unlocked_Scene, Coin_Payment
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
class AddUnderstoodSerializer(serializers.Serializer):
    word = serializers.CharField(required = True)
    target_point = serializers.IntegerField(required = True)
    scene_id = serializers.IntegerField(required = True)
    lookup_field = "user"
class PosRotSerializer(serializers.Serializer):
    model = Word
    id = serializers.IntegerField(required = True)
    position = serializers.CharField(required = True)
    rotation = serializers.CharField(required = True)


# class PercentageSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ["scene_name","percentage","total_vocab","complete"]
#         model = Percentage
class PercentageSerializer(serializers.Serializer):
    model = Percentage
    scene_name = serializers.CharField(required = True)
    percentage = serializers.IntegerField(required = True)
    total_vocab = serializers.IntegerField(required = True)
    complete = serializers.IntegerField(required = True)

class PercentageUpdatePercentageSerializer(serializers.Serializer):
    scene_name = serializers.CharField(required = True)
    percentage = serializers.IntegerField(required = True)

class PercentageUpdateCompleteSerializer(serializers.Serializer):
    scene_name = serializers.CharField(required = True)
    complete = serializers.IntegerField(required = True)

class PointToApproveSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = PointToApprove

class UpdateUserScoreSerializer(serializers.Serializer):
    percentage = serializers.IntegerField(required = True)
    coin = serializers.IntegerField(required = True)
    scene_id = serializers.IntegerField(required = True)

class UpdatePurchasedSceneSerializer(serializers.Serializer):
    scene_id = serializers.IntegerField(required = True)

class UnlockedSceneSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Unlocked_Scene

class CoinPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Coin_Payment

class UpdatePayCoinSerializer(serializers.Serializer):
    pay_coin = serializers.IntegerField(required = True)

class UpdateBuyCoinSerializer(serializers.Serializer):
    buy_coin = serializers.IntegerField(required = True)

class TopScoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = "user.username", read_only = True)
    class Meta:
        model = Coin_Payment
        fields = ('id','username','score')
