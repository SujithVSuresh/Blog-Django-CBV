from django.shortcuts import render
from django.views import View
from blogmain.models import BlogPost, Category

# Create your views here.

class Landing(View):
    def get(self, request, *args, **kwargs):

        #to show latest four posts.
        blog = BlogPost.objects.all().order_by('-id')[:4]

        category = Category.objects.all()

        context = {
            'blog':blog,
            'category':category
        }
        return render(request, 'landing/landing.html', context)

class TopicPost(View):
    def get(self, request, pk, *args, **kwargs):  

        topic_post = BlogPost.objects.filter(category=pk)  
        category = Category.objects.get(pk=pk)  

        context = {
            'topic_post':topic_post,
            'category':category
        }
        return render(request, 'landing/topic_post.html', context)        