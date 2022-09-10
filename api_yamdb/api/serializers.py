import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CHOICES, User


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


class TokenObtainPairEmailSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        read_only_fields = ('password',)
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username'),
                message='Такое название уже занято'
            )
        ]

    def validate(self, attrs):
        if attrs['email'] == attrs['username']:
            raise serializers.ValidationError(
                'Почта не может совадать с именем')
        elif attrs['username'] == 'me':
            raise serializers.ValidationError(
                'Имя не может быть равно me')
        super().validate()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.rating

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(TitleReadSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug')
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True)
    year = serializers.IntegerField(min_value=0,
                                    max_value=dt.datetime.now().year)

    def to_representation(self, instance):
        return instance

    class Meta:
        model = Title
        fields = '__all__'
