from rest_framework import serializers

from .models import Comment, Pattern, Vote


class PatternSerializer(serializers.ModelSerializer):
    prompt = serializers.CharField(write_only=True)
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
        validated_data.pop('prompt', None)
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_at', 'updated_at')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'vote_type', 'created_at')
