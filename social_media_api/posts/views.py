from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.response import Response
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


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
        following_users = user.profile.following.all()
        result = Post.objects.filter(author__in=following_users).order_by('-created_at')
        return result
    
class LikeViewSet(generics.GenericAPIView):
    permission_classes= [permissions.IsAuthenticated]

    def post(self, request, pk):
        post= generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response(status=400, data={'message': 'You already liked this post'})
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            content_type=ContentType.objects.get_for_model(post),
            object_id=post.id
        )
        return Response(status=201, data={'message': 'Post liked'})
    
class UnlikeViewSet(generics.GenericAPIView):
    permission_classes= [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post= Post.objects.get(id=post_id)
        like = Like.objects.filter(post=post, user=request.user).first()
        if not like:
            return Response(status=400, data={'message': 'You have not liked this post'})
        like.delete()
        return Response(status=201, data={'message': 'Post unliked'})


