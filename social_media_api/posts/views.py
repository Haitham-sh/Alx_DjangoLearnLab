from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes= [IsAuthenticated, IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 15
        
        posts = Post.objects.all().order_by('-created_at')
        result_page = paginator.paginate_queryset(posts, request)
        
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes= [IsAuthenticated, IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        
        posts = Post.objects.all().order_by('-created_at')
        result_page = paginator.paginate_queryset(posts, request)
        
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
def search_posts(request):
    search = request.GET.get('search', '')
    if search:
        posts = Post.objects.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )
    else:
        posts = Post.objects.none()
    return render(request, 'blog/search.html', {'posts': posts, 'search_term': search})

class FeedViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        result = Post.objects.filter(author__in=user.following.all()).order_by('-created_at')
        return result