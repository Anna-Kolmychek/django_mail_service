from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Article


class BlogListView(ListView):
    model = Article


class BlogDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        article = self.object
        article.views_count += 1
        article.save()
        return context_data

