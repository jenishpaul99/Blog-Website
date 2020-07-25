from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from blog.models import Post,LikedPost
from users.models import Profile
from django.contrib.auth.models import User
from django.views.generic import (ListView,
                                DetailView,
                                CreateView,
                                UpdateView,
                                DeleteView
                                )
from django_filters.views import FilterView
from .filters import PostFilter

def addLike(request,post_id,user_id):
    likedPosts=LikedPost.objects.filter(user_id=user_id).filter(post_id=post_id)
    print(likedPosts)
    # if post_id not in likedPosts:
    #     likedPosts.add(post_id)
    
    if len(likedPosts)==0:
        newLike=LikedPost(user_id=user_id,post_id=post_id)
        newLike.save()
        post=Post.objects.filter(id=post_id)
        likes=post.first().likes+1
        post.update(likes=likes)
    else:
        print('already liked')
        #add message to notify
    return redirect('detail-profile' ,pk=str(post_id))

def home(request):
    myFilter=PostFilter()
    context={'myFilter':myFilter}
    return render(request,'blog/home.html',context)

def search(request):
    post=Post.objects.all()
    myFilter=PostFilter(request.GET,queryset=post)
    post=myFilter.qs
    print(post)
    context={'myFilter':myFilter,'post':post}
    return render(request,'blog/searchPost.html',context)

class PostListView(ListView):
    model=Post
    context_object_name='posts'
    template_name='post_list.html' #modelName_viewType.html
    ordering=['-date']
    paginate_by=5

class PostList(FilterView):
    model = Post
    paginate_by=5    
    filter_class = PostFilter
    filterset_fields = {
            'title': ['icontains']#'nameoffield':['matchparameter']
            # 'label':'kjdhkfjd'
        }
    context_object_name = 'posts'
    template_name='blog/post_list.html' #modelName_viewType.html
    ordering=['-date']
    

class UserPostListView(ListView):
    model=User
    context_object_name='posts'
    template_name='user_posts.html' #modelName_viewType.html
    paginate_by=5 

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(name=user).order_by('-date')


class PostDetailView(DetailView):
    model=Post
    context_object_name='post'

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    template_name='blog/createPost.html'
    fields=['title','content']

    def form_valid(self, form):
        form.instance.name=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    template_name='blog/updatePost.html'
    fields=['title','content']

    def form_valid(self,form):
        form.instance.name=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post=self.get_object()
        if post.name == self.request.user:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if post.name == self.request.user:
            return True
        return False


def about(request):
    return render(request,'blog/about.html')
    
