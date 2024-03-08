from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Comment, Pattern, Vote
from .serializers import CommentSerializer, PatternSerializer, VoteSerializer


class PatternsListCreateView(ListCreateAPIView):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PatternsRetreiveDeleteView(RetrieveDestroyAPIView):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PatternCommentsListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pattern_id = self.kwargs['pk']
        return Comment.objects.filter(pattern_id=pattern_id)

    def perform_create(self, serializer):
        pattern_id = self.kwargs['pk']
        serializer.save(owner=self.request.user, pattern_id=pattern_id)


class PatternCommentRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_url_kwarg = 'ck'

    def get_queryset(self):
        pattern_id = self.kwargs['pk']
        return Comment.objects.filter(pattern_id=pattern_id)


class PatternVoteCreateView(CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        pattern_id = self.kwargs['pk']
        return Vote.objects.filter(pattern_id=pattern_id)

    def perform_create(self, serializer):
        pattern_id = self.kwargs['pk']
        serializer.save(user=self.request.user, pattern_id=pattern_id)


class PatternVoteUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        pattern_id = self.kwargs['pk']
        return Vote.objects.get(pattern_id=pattern_id, user=self.request.user)
