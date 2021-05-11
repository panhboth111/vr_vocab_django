from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Scene (models.Model):
    scene_name = models.CharField( max_length=200)
    scene_image = models.CharField( max_length=200)
    level = models.IntegerField()

class Word (models.Model):
    word = models.CharField( max_length=200 )
    pic = models.CharField( max_length=200 )
    audio = models.CharField( max_length=200 )
    synonym = models.CharField( max_length=200 )
    definition = models.TextField()
    example = models.TextField()
    position = models.CharField( max_length=255,default="" )
    rotation = models.CharField( max_length=255,default="" )
    scene = models.ForeignKey(Scene, related_name='words',on_delete=models.CASCADE)

class Bookmark(models.Model):
    word = models.CharField( max_length=200 )
    definition = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class Understood(models.Model):
    word = models.CharField( max_length=200 )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Percentage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    scene_name = models.CharField( max_length=200, null=True )
    percentage = models.CharField( max_length=200, null=True )
    total_vocab = models.CharField( max_length=200, null=True )
    complete = models.CharField( max_length=200, null=True )

class PointToApprove(models.Model):
    target_point = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Unlocked_Scene(models.Model):
    scene_name = models.CharField(max_length = 200, null = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)

class Coin_Payment(models.Model):
    coin = models.IntegerField(default = 0)
    score = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)