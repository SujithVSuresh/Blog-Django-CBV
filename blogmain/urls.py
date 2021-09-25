from .views import CommentReplyView, FollowPost, PostDislikeView, PostLikeView, ProfileEditView, ProfileView, PostDetailView, CreateBlogView, SearchPostView, SavedPostView, UnsavePostView, FollowView, UnfollowView, PostDeleteView, PostEditView, SearchPeopleView
from django.urls import path

urlpatterns = [
    path('', FollowPost.as_view(), name='blog-main'),
    path('search/post/', SearchPostView.as_view(), name='search-post'),
    path('search/profile/', SearchPeopleView.as_view(), name='search-people'),
    path('profile/<str:pk>', ProfileView.as_view(), name='profile'),
    path('profile/create/blog-post', CreateBlogView.as_view(), name='create-blog'),
    path('profile/edit/<str:pk>', ProfileEditView.as_view(), name='profile-edit'),
    path('blog-post/<str:pk>', PostDetailView.as_view(), name='post-detail'),
    path('blog-post/delete/<str:pk>', PostDeleteView.as_view(), name='post-delete'),
    path('blog-post/edit/<str:pk>', PostEditView.as_view(), name='post-edit'),
    path('blog-post/detail/save-post/<str:pk>', SavedPostView.as_view(), name='save-post'),
    path('blog-post/detail/unsave-post/<str:pk>', UnsavePostView.as_view(), name='unsave-post'),
    path('blog-post/detail/like/<str:pk>', PostLikeView.as_view(), name='post-like'),
    path('blog-post/detail/dislike/<str:pk>', PostDislikeView.as_view(), name='post-dislike'),
    path('blog-post/detail/comment/<str:pk>/comment-reply', CommentReplyView.as_view(), name='comment-reply'),
    path('profile/follow/<str:pk>', FollowView.as_view(), name='follow'),
    path('profile/unfollow/<str:pk>', UnfollowView.as_view(), name='unfollow'),
]

