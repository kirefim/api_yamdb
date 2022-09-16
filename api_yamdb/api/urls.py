from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, get_jwt_token,
                    register_user)

v1_router = DefaultRouter()
v1_router.register(
    r'^titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(
    r'^titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(r'^genres', GenreViewSet, basename='genre')
v1_router.register(r'^categories', CategoryViewSet, basename='category')
v1_router.register(r'^titles', TitleViewSet, basename='title')
v1_router.register(r'^users', UserViewSet, basename='user')

urlpatterns = [
    re_path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', register_user, name='register'),
    path('v1/auth/token/', get_jwt_token, name='token'),
]
