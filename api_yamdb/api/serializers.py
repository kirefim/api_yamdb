from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('reviewer', 'title',),
                message='На это произведение Вы уже оставляли отзыв.',),
        )
