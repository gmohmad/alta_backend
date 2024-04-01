from rest_framework import serializers

from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    initiator = serializers.PrimaryKeyRelatedField(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(read_only=True)
    error = serializers.CharField(allow_blank=True, required=False, read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'initiator', 'receiver', 'created_at', 'error')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'body', 'chat', 'updated_at', 'created_at')
        read_only_fields = ('sender', 'chat')
