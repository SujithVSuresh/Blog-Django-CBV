from django import views
from django.core.checks.messages import CRITICAL
from django.db.models.expressions import Value
from blogmain.models import UserProfile, BlogPost
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CommentReplyForm, ProfileUpdateForm, CreateBlogPostForm, PostCommentForm
from .models import BlogPost, Comment, CommentReply
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect

# Create your views here.
class FollowPost(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        following_user = UserProfile.objects.get(username=request.user)
        user_following = following_user.following.all()
        posts = BlogPost.objects.filter(author__in=user_following).order_by('-posted_on')

        context = {
            'posts':posts

        }
        return render(request, 'blogmain/blog_post.html', context)

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post_detail = BlogPost.objects.get(id=pk)
        profile = UserProfile.objects.get(username=request.user)
        post_save = profile.saved_post.all()
        comment_reply = CommentReply.objects.filter()

        comment_form = PostCommentForm()

        comment_show = Comment.objects.filter(post=pk)


        if len(post_save) == 0:
            is_saved = False

        for post in post_save:
            if post == post_detail:
                is_saved = True
                break
            else:
                is_saved = False


        context = {
            'post_detail':post_detail,
            'is_saved':is_saved,
            'comment_form':comment_form,
            'comment_show':comment_show

        }
        return render(request, 'blogmain/post_detail.html', context)   

    def post(self, request, pk, *args, **kwargs):
        post_detail = BlogPost.objects.get(id=pk)
        profile = UserProfile.objects.get(username=request.user)
        post_save = profile.saved_post.all()

        comment = PostCommentForm(request.POST)

        if comment.is_valid():
            new_comment = comment.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post_detail
            new_comment.save()
            return redirect('post-detail', pk=pk)    


        if len(post_save) == 0:
            is_saved = False

        for post in post_save:
            if post == post_detail:
                is_saved = True
                break
            else:
                is_saved = False


        context = {
            'post_detail':post_detail,
            'is_saved':is_saved,

        }
        return render(request, 'blogmain/post_detail.html', context)

class CommentReplyView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(id=pk)
        comment_reply_form = CommentReplyForm()
        comment_reply = CommentReply.objects.filter(comment=pk)

        context = {
            'comment':comment,
            'form':comment_reply_form,
            'comment_reply':comment_reply

        }
        return render(request, 'blogmain/comment_reply.html', context)   

    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(id=pk)
        comment_reply = CommentReply.objects.filter(comment=pk)

        comment_reply_form = CommentReplyForm(request.POST)
        if comment_reply_form.is_valid():
            reply = comment_reply_form.save(commit=False)
            reply.author = request.user
            reply.comment = comment
            reply.save()
            return redirect('comment-reply', pk=pk)

        context = {
            'comment':comment,
            'comment_reply':comment_reply

        }
        return render(request, 'blogmain/comment_reply.html', context)      

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blogmain/delete_post.html'
    success_url = reverse_lazy('blog-main')

class PostEditView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'blogmain/edit_post.html'
    form_class = CreateBlogPostForm
    success_url = reverse_lazy('blog-main')    
            

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(username=pk)
        post_save = profile.saved_post.all()
        blog_post = BlogPost.objects.filter(author=pk)
        followers = profile.follower.all()
        following_count = profile.following.all().count()
        follower_count = followers.count()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False     
  
        context = {
            'profile':profile,
            'blog_post':blog_post,
            'post_save':post_save,
            'is_following':is_following,
            'follower_count':follower_count,
            'following_count':following_count
        }
        return render(request, 'blogmain/profile.html', context)  
              
class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(username=pk)
        form = ProfileUpdateForm(instance=profile)

        context = {
            'form':form

        }
        return render(request, 'blogmain/profile_edit.html', context)

    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(username=pk)
        form = ProfileUpdateForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.warning(request, 'Your profile updated successfully..')
            return redirect('profile', pk=request.user.pk)

        context = {
            'form':form
        }
        return render(request, 'blogmain/profile_edit.html', context)

class CreateBlogView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = BlogPost
    template_name = 'blogmain/create_blog.html'
    form_class = CreateBlogPostForm
    success_message = 'Blog post created successfully..'
    success_url = reverse_lazy('blog-main')   


    def get_initial(self):
        return {'author':self.request.user}

class SearchPostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query', 'value')

        post_list = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(meta_description__icontains=query)
        )


        context = {
            'post_list':post_list,
        }
        return render(request, 'blogmain/search_post.html', context)

        
class SearchPeopleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query', 'value')

        profile_list = UserProfile.objects.filter(
            Q(name__icontains=query)
        )


        context = {
            'profile_list':profile_list,
        }
        return render(request, 'blogmain/search_people.html', context)

class SavedPostView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = BlogPost.objects.get(pk=pk)
        user_profile = UserProfile.objects.get(username=request.user)
        user_profile.saved_post.add(post)
        messages.success(request, 'Post saved successfully..')
        return redirect('post-detail', pk=post.pk)
        

class UnsavePostView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = BlogPost.objects.get(pk=pk)
        user_profile = UserProfile.objects.get(username=request.user)
        user_profile.saved_post.remove(post)
        messages.warning(request, 'Post removed from saved list..')
        return redirect('post-detail', pk=post.pk)

class FollowView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        #follower
        profile = UserProfile.objects.get(username=pk)
        profile.follower.add(request.user)
        
        #following
        profile_following = User.objects.get(id=pk)
        user_profile = UserProfile.objects.get(username=request.user)
        user_profile.following.add(profile_following)

        return redirect('profile', pk=profile.username.pk)

class UnfollowView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        #follower
        profile = UserProfile.objects.get(username=pk)
        profile.follower.remove(request.user)
        
        #following
        profile_following = User.objects.get(id=pk)
        user_profile = UserProfile.objects.get(username=request.user)
        user_profile.following.remove(profile_following)

        return redirect('profile', pk=profile.username.pk)

class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = BlogPost.objects.get(id=pk)

        is_dislike = False

        for dislike in post.dislike.all():
            if dislike == request.user:
                is_dislike = True

        if is_dislike:
            post.dislike.remove(request.user)

        
        is_like = False

        for like in post.like.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.like.add(request.user)
            messages.success(request, 'You like this post')     

        if is_like:
            post.like.remove(request.user) 
            messages.success(request, 'like removed')
   

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)              


class PostDislikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = BlogPost.objects.get(id=pk)

        is_like = False

        for like in post.like.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.like.remove(request.user) 

        is_dislike = False

        for dislike in post.dislike.all():
            if dislike == request.user:
                is_dislike = True

        if not is_dislike:
            post.dislike.add(request.user)
            messages.warning(request, 'You dislike this post')   

        if is_dislike:
            post.dislike.remove(request.user)  
            messages.success(request, 'Dislike removed')

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)              






       
    


