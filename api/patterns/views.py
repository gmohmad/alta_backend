from drf_spectacular.utils import extend_schema
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
from .permissions import IsOwnerOrReadOnly
from .serializers import CommentSerializer, PatternSerializer, VoteSerializer


@extend_schema(
    tags=['Patterns'],
    description='List all the patterns or create a new pattern if logged in'
)
class PatternsListCreateView(ListCreateAPIView):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema(
    tags=['Patterns'],
    description='Get or delete specified pattern if logged in and if is the owner of this pattern'
)
class PatternsRetreiveDeleteView(RetrieveDestroyAPIView):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer
    permission_classes = (IsOwnerOrReadOnly,)


@extend_schema(
    tags=['Comments'],
    description='List all the comments of a pattern or create a new comment if logged in'
)
class PatternCommentsListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        pattern_id = self.kwargs['pk']
        return Comment.objects.filter(pattern_id=pattern_id)

    def perform_create(self, serializer):
        pattern_id = self.kwargs['pk']
        serializer.save(owner=self.request.user, pattern_id=pattern_id)


@extend_schema(
    tags=['Comments'],
    # exclude=['PATCH'],
    description='Get or update/delete a comment if logged in and if is the owner of this comment'
)
class PatternCommentRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_url_kwarg = 'ck'

    def get_queryset(self):
        pattern_id = self.kwargs['pk']
        return Comment.objects.filter(pattern_id=pattern_id)


@extend_schema(
    tags=['Votes'],
    description='Create a vote if logged in and if havent created a vote on this pattern already'
)
class PatternVoteCreateView(CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        pattern_id = self.kwargs['pk']
        return Vote.objects.filter(pattern_id=pattern_id)

    def perform_create(self, serializer):
        pattern_id = self.kwargs['pk']
        serializer.save(user=self.request.user, pattern_id=pattern_id)


@extend_schema(
    tags=['Votes'],
    # exclude=['PATCH'],
    description='Update/delete a vote if logged and if is the owner of this vote'
)
class PatternVoteUpdateDeleteView(UpdateAPIView, DestroyAPIView):
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        pattern_id = self.kwargs['pk']
        return Vote.objects.get(pattern_id=pattern_id, user=self.request.user)
