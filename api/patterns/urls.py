from django.urls import path

from .views import (
    PatternCommentsListCreateView,
    PatternsCommentRUDView,
    PatternsListCreateView,
    PatternsRetreiveDeleteView,
)

urlpatterns = [
    path('', PatternsListCreateView.as_view(), name='pattern-list-create'),
    path('<str:pk>/', PatternsRetreiveDeleteView.as_view(), name='pattern-retrieve-delete'),
    path('<str:pk>/comments/', PatternCommentsListCreateView.as_view(), name='comment-list-create'),
    path('<str:pk>/comments/<str:ck>/', PatternsCommentRUDView.as_view(), name='comment-rud'),
]
