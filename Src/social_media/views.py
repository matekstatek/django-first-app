from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import Post

# Create your views here.
# funkcja wywołująca home.html razem z postami, które zostały stworzone
# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'social_media/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'social_media/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'social_media/about.html', {'title': "About"})
