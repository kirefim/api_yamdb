from django.urls import path

from rest_framework import routers

from .views import TokenObtainPairConfirmEmailView, GetTokenView


router_v1 = routers.DefaultRouter()

urlpatterns = [
    path('v1/auth/signup/', TokenObtainPairConfirmEmailView.as_view(),
         name='token_obtain_pair_not_conform'),
    path('v1/auth/token/', GetTokenView.as_view(),
         name='get_token'),
]
