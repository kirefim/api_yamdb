from django.urls import path
from rest_framework import routers

from .views import (GetTokenView, TokenObtainPairConfirmEmailView,
                    UserList, UserDetail)

router_v1 = routers.DefaultRouter()

urlpatterns = [
     path('v1/auth/signup/', TokenObtainPairConfirmEmailView.as_view(),
          name='token_obtain_pair_not_conform'),
     path('v1/auth/token/', GetTokenView.as_view(),
          name='get_token'),
     path('users/', UserList.as_view(), name='users_list'),
     path('users/<str:username>/', UserDetail.as_view(), name='users_detail'),
     path('users/me/', UserDetail.as_view(), name='users_me'),
]
