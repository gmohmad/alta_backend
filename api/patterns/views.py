from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment, Pattern
from .serializers import CommentSerializer, PatternSerializer


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


class PatternsCommentRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_url_kwarg = 'ck'

    def get_queryset(self):
        pattern_id = self.kwargs['pk']
        return Comment.objects.filter(pattern_id=pattern_id)
