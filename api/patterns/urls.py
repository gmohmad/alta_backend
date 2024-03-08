from django.urls import path

from .views import (
    PatternCommentRUDView,
    PatternCommentsListCreateView,
    PatternsListCreateView,
    PatternsRetreiveDeleteView,
    PatternVoteCreateView,
    PatternVoteUpdateDeleteView,
)

urlpatterns = [
    path('', PatternsListCreateView.as_view(), name='pattern-list-create'),
    path('<str:pk>/', PatternsRetreiveDeleteView.as_view(), name='pattern-retrieve-delete'),

    path('<str:pk>/comments/', PatternCommentsListCreateView.as_view(), name='comment-list-create'),
    path('<str:pk>/comments/<str:ck>/', PatternCommentRUDView.as_view(), name='comment-rud'),

    path('<str:pk>/votes/', PatternVoteCreateView.as_view(), name='vote-create'),
    path('<str:pk>/vote-upd-del/', PatternVoteUpdateDeleteView.as_view(), name='vote-upd-del'),
]
