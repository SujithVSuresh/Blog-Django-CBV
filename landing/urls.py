from django.urls import path
from .views import Landing, TopicPost

urlpatterns = [
    path('', Landing.as_view(), name='landing'),
    path('topic/<str:pk>/', TopicPost.as_view(), name='topic-post')
]