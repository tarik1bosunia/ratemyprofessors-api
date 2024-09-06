from rest_framework import viewsets, generics
from .models import Content, Comment, Like
from .serializers import ContentSerializer, CommentSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        content_id = self.kwargs['content_id']
        return Comment.objects.filter(content_id=content_id)