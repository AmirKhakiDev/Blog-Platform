from rest_framework import serializers
from .models import BlogPost, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class BlogPostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "author",
            "title",
            "slug",
            "category",
            "content",
            "created_at",
            "updated_at",
            "is_published",
        ]
        read_only_fields = ["created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(read_only=True)
    post = serializers.SlugRelatedField(queryset=BlogPost.objects.all(), slug_field="slug")

    class Meta:
        model = Comment
        fields = ["id", "post", "username", "email", "content", "created_at", "is_approved"]
        read_only_fields = ["created_at"]

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value
