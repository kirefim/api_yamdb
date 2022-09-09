from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .permissions import IsAdminModeratorOwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
)
from reviews.models import Review, Title

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAdminModeratorOwnerOrReadOnly,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAdminModeratorOwnerOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            review_id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review=review)
