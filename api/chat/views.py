from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Chat, Message
from .permissions import IsOwner
from .serializers import ChatSerializer, MessageSerializer

# Create your views here.


class ChatListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(Q(initiator=self.request.user) | Q(receiver=self.request.user))


class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        receiver_id = self.kwargs['pk']
        participant = get_object_or_404(User, pk=receiver_id)

        chat = Chat.objects.filter(Q(initiator=self.request.user, receiver=participant) |
                                   Q(initiator=participant, receiver=self.request.user))

        if chat.exists():
            raise ValidationError('You already have a chat with this user.')
        if int(receiver_id) == self.request.user.id:
            raise ValidationError("You can't create a chat with yourself")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, participant)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, participant):
        serializer.save(initiator=self.request.user, receiver=participant)


class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (IsOwner,)


class MessageListCreateView(ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        chat_id = self.kwargs['pk']
        return Message.objects.filter(chat_id=chat_id)

    def perform_create(self, serializer):
        chat_id = self.kwargs['pk']
        serializer.save(chat_id=chat_id, sender=self.request.user)


class MessageRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        chat_id = self.kwargs['ck']
        return Message.objects.filter(chat_id=chat_id)
