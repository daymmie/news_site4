from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_choice',
            'post_title',
            'post_text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("post_title")
        text = cleaned_data.get("post_text")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data
