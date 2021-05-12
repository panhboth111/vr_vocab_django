from django.contrib import admin
from .models import Word, Scene, Percentage, Bookmark, Understood, PointToApprove, Unlocked_Scene , Coin_Payment
# Register your models here.
admin.site.register(Word)
admin.site.register(Scene)
admin.site.register(Percentage)
admin.site.register(Bookmark)
admin.site.register(Understood)
admin.site.register(PointToApprove)
admin.site.register(Unlocked_Scene)
admin.site.register(Coin_Payment)

