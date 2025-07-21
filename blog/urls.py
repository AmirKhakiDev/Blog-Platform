from django.urls import path
from .views import BlogPostView, CommentView, ObtainToken

urlpatterns = [
    path('blog/', BlogPostView.as_view(), name='blog_post'),
    path('blog/<str:slug>/', BlogPostView.as_view(), name='blog_post_detail'),
    
    path('blog/<slug:slug>/comments/', CommentView.as_view(), name='post-comments'),

    path('comment/', CommentView.as_view(), name='comment_post'),
    path('auth-token/', ObtainToken.as_view(), name='token')
]
