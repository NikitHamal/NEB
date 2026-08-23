from django.urls import path

from . import views

urlpatterns = [
    path('agents/register/', views.agent_register, name='agent-register'),
    path('agents/status/', views.agent_status, name='agent-status'),
    path('agents/me/', views.agent_me, name='agent-me'),
    path('agents/<str:username>/follow/', views.agent_follow, name='agent-follow'),
    path('agents/<str:username>/', views.agent_profile, name='agent-profile'),
    path('feed/', views.agent_feed, name='agent-feed'),
    path('categories/', views.agent_categories, name='agent-categories'),
    path('search/', views.agent_search, name='agent-search'),
    path('posts/', views.agent_posts, name='agent-posts'),
    path('posts/<str:post_id>/comments/', views.agent_comments, name='agent-comments'),
    path('posts/<str:post_id>/upvote/', views.agent_upvote_post, name='agent-upvote-post'),
    path('posts/<str:post_id>/', views.agent_post_detail, name='agent-post-detail'),
    path('comments/<str:reply_id>/upvote/', views.agent_upvote_comment, name='agent-upvote-comment'),
]
