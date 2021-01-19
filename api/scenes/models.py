from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Scene (models.Model):
    scene_name = models.CharField( max_length=20)
    scene_image = models.CharField( max_length=20)
    level = models.IntegerField()

class Word (models.Model):
    word = models.CharField( max_length=20 )
    pic = models.CharField( max_length=20 )
    audio = models.CharField( max_length=20 )
    synonym = models.CharField( max_length=20 )
    definition = models.TextField()
    example = models.TextField()
    scene = models.ForeignKey(Scene, related_name='words',on_delete=models.CASCADE)

class Bookmark(models.Model):
    word = models.CharField( max_length=20 )
    definition = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class Percentage(models.Model):
    scene_name = models.CharField( max_length=20 )
    percentage = models.IntegerField()
    total_vocab = models.IntegerField()
    complete = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class Understood(models.Model):
    word = models.CharField( max_length=20 )
    user = models.ForeignKey(User, on_delete=models.CASCADE)


