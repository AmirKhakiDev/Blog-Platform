from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

from .models import BlogPost, Category, Comment
from .serializers import BlogPostSerializer, CommentSerializer, CategorySerializer

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class BlogPostView(GenericAPIView, CreateModelMixin):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        if "slug" in kwargs:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            queryset = BlogPost.objects.filter(author=request.user)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CommentView(GenericAPIView, CreateModelMixin):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            return Comment.objects.filter(post__slug=slug)
        return Comment.objects.all()

    @method_decorator(cache_page(40))
    @method_decorator(vary_on_cookie)
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)


class ObtainToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
