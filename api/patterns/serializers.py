from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Comment, Pattern, Vote
from .utils import generate_img


class PatternSerializer(serializers.ModelSerializer):
    prompt = serializers.CharField(write_only=True)
    image_url = serializers.URLField(read_only=True)
    rating = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = Pattern
        fields = (
            'id',
            'prompt',
            'image_url',
            'rating',
            'created_at',
            'updated_at',
        )

    def create(self, validated_data):
        image_url = generate_img(validated_data.pop('prompt', None))
        instance = super().create(validated_data)

        instance.image_url = image_url
        instance.save()

        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_at', 'updated_at')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'vote_type', 'created_at')
