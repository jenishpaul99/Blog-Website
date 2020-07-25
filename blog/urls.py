from django.urls import path
from . import views
from blog.views import (PostListView,
                        PostDetailView,
                        PostCreateView,
                        PostUpdateView,
                        PostDeleteView,
                        UserPostListView,
                        PostList 
                        )
urlpatterns = [
    path('', PostList.as_view(),name='blog-home'),
    path('search/', views.search,name='search-post'),
    path('post/create/',PostCreateView.as_view(),name='create-post'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='detail-profile'),
    path('post/<str:username>/',UserPostListView.as_view(),name='user-posts'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='update-post'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='delete-post'),
    path('addLike/(<int:post_id>,<int:user_id>)',views.addLike,name='add-like'),
    path('about/',views.about,name='blog-about')
]