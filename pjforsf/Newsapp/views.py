from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = '-post_date'
    template_name = 'news.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail_view.html'
    context_object_name = 'post_detail'


class PostSearch(ListView):
    model = Post
    ordering = '-post_date'
    template_name = 'search.html'
    context_object_name = 'post_search'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    permission_required = (
        'Newsapp.add_post',
        'Newsapp.change_post',
    )
    model = Post
    template_name = 'post_create.html'


class PostUpdate(UpdateView, PermissionRequiredMixin):
    form_class = PostForm
    permission_required = (
        'Newsapp.add_post',
        'Newsapp.change_post',
    )
    model = Post
    template_name = 'post_create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
