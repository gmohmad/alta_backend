from django.contrib.auth.models import User
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework import status
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

@extend_schema(
    tags=['Chats'],
    description='List all the chats of the authenticated user'
)
class ChatListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(Q(initiator=self.request.user) | Q(receiver=self.request.user))

@extend_schema(
    tags=['Chats'],
    description='Create a chat'
)
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
            return Response({'message': 'You already have a chat with this user.'}, status=status.HTTP_400_BAD_REQUEST)
        if int(receiver_id) == self.request.user.id:
            return Response({'message': 'You cannot create a chat with yourself.'}, status=status.HTTP_400_BAD_REQUEST)


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, participant)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, participant):
        serializer.save(initiator=self.request.user, receiver=participant)

@extend_schema(
    tags=['Chats'],
    description='Delete a chat'
)
class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (IsOwner,)

@extend_schema(
    tags=['Messages'],
    description='List all the messages in chat or create one'
)
class MessageListCreateView(ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        chat_id = self.kwargs['pk']
        return Message.objects.filter(chat_id=chat_id)

    def perform_create(self, serializer):
        chat_id = self.kwargs['pk']
        serializer.save(chat_id=chat_id, sender=self.request.user)

@extend_schema(
    tags=['Messages'],
    description='Retrieve/update/delete a message'
)
class MessageRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        chat_id = self.kwargs['ck']
        return Message.objects.filter(chat_id=chat_id)
