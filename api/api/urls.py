from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt import views as jwt_views
from accounts.views import UserViewSet, PaymentViewSet
from scenes.views import SceneViewSet, WordViewSet, BookmarkViewSet, RecommendationViewSet, UnderstoodViewSet, PercentageViewSet, PointToApproveViewSet


router = routers.SimpleRouter()
router.register('accounts', UserViewSet)
router.register('scenes', SceneViewSet)
router.register('words', WordViewSet)
router.register('bookmarks', BookmarkViewSet)
router.register('recommendations', RecommendationViewSet)
router.register('understoods', UnderstoodViewSet)
router.register('percentage',PercentageViewSet)
router.register('points', PointToApproveViewSet)
router.register('payment', PaymentViewSet, basename="payment")


schema_view = get_swagger_view(title="VR Vocabulary API Documentation"  )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('documentation/',schema_view),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    
]