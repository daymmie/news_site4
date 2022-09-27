from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'post_title': ['exact'],
            'post_category': ['exact']
        }
