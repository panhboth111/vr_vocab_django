from django.shortcuts import render
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Scene,Word,Bookmark,Understood, Percentage, PointToApprove, Unlocked_Scene, Coin_Payment, Purchased_Scene
from .serializers import SceneSerializer,WordSerializer,BookmarkSerializer, UnderstoodSerializer, PosRotSerializer, PercentageSerializer, PercentageUpdateCompleteSerializer, PercentageUpdatePercentageSerializer, PointToApproveSerializer, UpdateUserScoreSerializer, AddUnderstoodSerializer , UnlockedSceneSerializer, CoinPaymentSerializer, UpdatePayCoinSerializer, UpdateBuyCoinSerializer, UpdatePurchasedSceneSerializer, PurchasedSceneSerializer
from .mixins import GetSerializerClassMixin
from django.contrib.auth import get_user_model
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
# Create your views here.

User = get_user_model()
class SceneViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    list:
    get all the scenes
    retrieve:
    get all the scenes in a specific level. replace {id} with the number of level
    """
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    serializer_action_classes = {
        'update_purchased_scene': UpdatePurchasedSceneSerializer
    }
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
        scenes = set([word.scene for word in words if word.position == "non" or word.rotation == "non"])
        serializer = self.get_serializer(scenes,many=True)
        return Response(serializer.data)

    @action(detail = False, methods = ['post'], url_path = 'purchased_scene')
    def update_purchased_scene(self, request):
        """
            update scene_id that already buy
        """
        user = request.user
        serializer = UpdatePurchasedSceneSerializer(data = request.data)
        if serializer.is_valid():
            purchased_scene = Purchased_Scene(scene_id = serializer.data.get("scene_id"), user = user)
            purchased_scene.save()
            coin_payment = Coin_Payment.objects.filter(user = user)
            if coin_payment.exists():
                queried_coin = Coin_Payment.objects.get(user = user.id)
                if queried_coin.coin >= 5:
                    queried_coin.coin -= 5
                    queried_coin.save()
                else: return Response("You don't have enough coin!")
            else: 
                return Response("You don't have any coin yet! Purchase some?")
            return Response("Scene updated successfully!")
        return Response(serializer.errors)

    @action(detail = False, methods=['get'], permission_classes = [IsAuthenticated])
    def purchased_scene(self, request):
        """
            Query record from purchased_scene table by user
        """
        user = request.user
        scene = Purchased_Scene.objects.filter(user = user)
        serializer = PurchasedSceneSerializer(scene, many = True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes = [IsAuthenticated])
    def unlock_scene(self, request):
        user = request.user
        userdatas = User.objects.get(id=user.id)
        if user.sub_plan == "Bronze":
            queried_percentage = Percentage.objects.all()
            queried_purchased_scene = Purchased_Scene.objects.all()
            queried_percentage_scene_names = [s.scene_name for s in queried_percentage]
            queried_purchased_scene_names = [s.scene_id for s in queried_purchased_scene]
            queried_scenes = Scene.objects.all().filter(~Q(scene_name__in = queried_percentage_scene_names), ~Q(id__in = queried_purchased_scene_names), level=user.level)[:1]
            serializer = SceneSerializer(queried_scenes, many=True)
            scene_names = [data.scene_name for data in queried_scenes]
            if(datetime.now().date() == user.last_request.date()):
                # userdatas.last_request = userdatas.sub_date
                # userdatas.save()
                queried_unlock_scene = Unlocked_Scene.objects.all().filter(user = user.id)
                serializer = UnlockedSceneSerializer(queried_unlock_scene, many = True)
                return Response(serializer.data)
            else:
                userdatas.last_request = datetime.now().date()
                userdatas.save()
                for scene_name in scene_names:
                    percentage_scene = Percentage(user = user, scene_name = scene_name)
                    percentage_scene.save()
                    try:
                        unlock_scene_data = Unlocked_Scene.objects.get(user = user.id)
                        unlock_scene_data.scene_name = scene_name
                        unlock_scene_data.save()
                    except:
                        unlock_scene = Unlocked_Scene(user = user, scene_name = scene_name)
                        unlock_scene.save()
                return Response(serializer.data)
        if user.sub_plan == "Silver":
            expire_date = user.sub_date + relativedelta(months=3)
            if(datetime.now().date() == expire_date.date()):
                return Response("Payment expire")
            else :
                queried_percentage = Percentage.objects.all()
                queried_percentage_scene_names = [s.scene_name for s in queried_percentage]
                queried_scenes = Scene.objects.all().filter(~Q(scene_name__in=queried_percentage_scene_names),level=user.level)[:2]
                serializer = SceneSerializer(queried_scenes,many=True)
                scene_names = [data.scene_name for data in queried_scenes]
                if(datetime.now().date() == user.last_request.date()):
                    queried_unlock_scene = Unlocked_Scene.objects.all().filter(user = user.id)
                    serializer = UnlockedSceneSerializer(queried_unlock_scene, many = True)
                    return Response(serializer.data)
                else :
                    userdatas.last_request = datetime.now().date()
                    userdatas.save()
                    for scene_name in scene_names:
                        percentage_scene = Percentage(user = user, scene_name = scene_name)
                        percentage_scene.save()
                        unlock_scene = Unlocked_Scene(user = user, scene_name = scene_name)
                        unlock_scene.save()
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
        """
            query recommendation scene from scene table base on level
        """
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
        """
            create & update <word> to understood table, 
        """
        user = request.user
        serializer = AddUnderstoodSerializer(data = request.data)
        if serializer.is_valid():
            understood = Understood(word=serializer.data.get("word"),user=user)
            understood.save()
            point = PointToApprove.objects.filter(user = user, scene_id = serializer.data.get("scene_id"))
            if point.exists():
                point = PointToApprove.objects.get(user = user, scene_id = serializer.data.get("scene_id"))
                point.target_point += serializer.data.get("target_point")
                point.save()
            else:
                create_point_to_approve = PointToApprove(target_point = serializer.data.get("target_point"), user = user, scene_id = serializer.data.get("scene_id"))
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
        'create': PercentageSerializer,
        'update_percentage':PercentageUpdatePercentageSerializer,
        'update_complete':PercentageUpdateCompleteSerializer
    }
    def create(self,request):
        """
            this endpoint will create the new record of current user if scene_name doesn't exist
        """
        user = request.user
        serializer = PercentageSerializer(data = request.data)
        if serializer.is_valid():
            queried_percentage = Percentage.objects.filter(user=user.id,scene_name=serializer.data.get("scene_name"))
            if queried_percentage.exists():
                return Response("The percentage for this user in this scene has already been created")
            new_percentage = Percentage(scene_name=serializer.data.get("scene_name"),user=user,percentage=serializer.data.get("percentage"), total_vocab=serializer.data.get("total_vocab"), complete=serializer.data.get("complete"))
            new_percentage.save()
            serializer = self.get_serializer(new_percentage)
            return Response(serializer.data)
        return Response(serializer.errors)
    def list(self,request):
        user = request.user
        percentage = Percentage.objects.all().filter(user=user.id)
        serializer = self.get_serializer(percentage, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['post'])
    def update_percentage(self,request):
        """
            update new percentage to percentage table
        """
        user = request.user
        serializer = PercentageUpdatePercentageSerializer(data = request.data)
        if serializer.is_valid():
            percentage = Percentage.objects.get(user=user.id,scene_name=serializer.data.get("scene_name"))
            percentage.percentage = serializer.data.get("percentage")
            percentage.save()
            return Response("percentage updated successfully")
        return Response(serializer.errors)
    @action(detail=False, methods=['post'])
    def update_complete(self,request):
        """
            update complete to percentage table
        """
        user = request.user
        serializer = PercentageUpdateCompleteSerializer(data = request.data)
        if serializer.is_valid():
            percentage = Percentage.objects.get(user=user.id,scene_name=serializer.data.get("scene_name"))
            percentage.complete = serializer.data.get("complete")
            percentage.save()
            return Response("complete updated successfully")
        return Response(serializer.errors)

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
        """
            Update coin & score that calculate with target_point to coin_payment table
        """
        user = request.user
        serializer = UpdateUserScoreSerializer(data = request.data)
        if serializer.is_valid():
            queried_user = User.objects.get(id = user.id)
            queried_point = PointToApprove.objects.get(user = user.id, scene_id = serializer.data.get("scene_id"))
            final_score = (queried_point.target_point * serializer.data.get("percentage"))/100
            coin_payment = Coin_Payment.objects.filter(user = user)
            if coin_payment.exists():
                coin_payment = Coin_Payment.objects.get(user = user)
                coin_payment.score += final_score
                coin_payment.save()
                coin_payment.coin += serializer.data.get("coin")
                coin_payment.save()

                queried_point.target_point = 0
                queried_point.save()
            else:
                coin_payment = Coin_Payment(coin = serializer.data.get("coin"), score = final_score, user = user)
                coin_payment.save()
            serializer = CoinPaymentSerializer(coin_payment)
            return Response(serializer.data)
        return Response(serializer.errors)

class CoinPaymentViewset(GetSerializerClassMixin,viewsets.ModelViewSet):
    queryset = Coin_Payment.objects.all()
    serializer_class = CoinPaymentSerializer
    permission_classes = [IsAuthenticated]
    serializer_action_classes = {
        'pay_coin': UpdatePayCoinSerializer,
        'buy_coin': UpdateBuyCoinSerializer
    }
    def list(self, request):
        user = request.user
        coin = Coin_Payment.objects.filter(user = user)
        serializer = CoinPaymentSerializer(coin, many = True)
        return Response(serializer.data[0])

    @action(detail=False, methods=['post'])
    def pay_coin(self, request):
        """
            use when user pay coin on scenes or other
        """
        user = request.user
        serializer = UpdatePayCoinSerializer(data = request.data)
        if serializer.is_valid():
            queried_user = User.objects.get(id = user.id)
            coin_payment = Coin_Payment.objects.filter(user = user.id)
            if coin_payment.exists():
                queried_coin = Coin_Payment.objects.get(user = user.id)
                if serializer.data.get("pay_coin") > queried_coin.coin:
                    return Response("You don't have enough coin!")
                queried_coin.coin -= serializer.data.get("pay_coin")
                queried_coin.save()
                return Response("You paid: " + str(serializer.data.get("pay_coin")) + " coins")
            else: return Response("You don't have any coin yet! Purchase some?")
        return Response(serializer.errors)
    @action(detail=False, methods=['post'])
    def buy_coin(self, request):
        """
            use when user purchase coin
        """
        user = request.user
        serializer = UpdateBuyCoinSerializer(data = request.data)
        if serializer.is_valid():
            coin_payment = Coin_Payment.objects.filter(user = user)
            if coin_payment.exists():
                queried_coin = Coin_Payment.objects.get(user = user.id)
                queried_coin.coin += serializer.data.get('buy_coin')
                queried_coin.save()
                return Response("Update buy coin successfully")
            else:
                coin_payment = Coin_Payment(coin = serializer.data.get("buy_coin"), score = 0, user = user)
                coin_payment.save()
                return Response("Purchased coin successfully")
        return Response(serializer.errors)
