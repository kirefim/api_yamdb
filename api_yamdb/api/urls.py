from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenView, ReviewViewSet, TitleViewSet,
                    TokenObtainPairConfirmEmailView, UserDetail, UserList)

v1_router = SimpleRouter()
v1_router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(
    'titles/(?P<title_id>\\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(r'genres', GenreViewSet, basename='genre')
v1_router.register(r'categories', CategoryViewSet, basename='category')
v1_router.register(r'titles', TitleViewSet, basename='title')


urlpatterns = [
    path('v1/auth/signup/', TokenObtainPairConfirmEmailView.as_view(),
         name='token_obtain_pair_not_conform'),
    path('v1/auth/token/', GetTokenView.as_view(),
         name='get_token'),
    path('users/', UserList.as_view(), name='users_list'),
    path('users/<str:username>/', UserDetail.as_view(), name='users_detail'),
    path('users/me/', UserDetail.as_view(), name='users_me'),
    path('v1/', include(v1_router.urls)),
]
