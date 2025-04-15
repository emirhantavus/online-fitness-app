from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Post,Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import permissions
from rest_framework import filters

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]  # Anonim kullanıcıların görmesini sağlar
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__first_name', 'author__last_name']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)