from django import forms
from .models import ShareBites, Comment

class ShareBitesForm(forms.ModelForm):
    class Meta:
        model = ShareBites
        fields = ['title', 'content', 'image', 'calorie_content', 'sugar_content', 'diet_type']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add a comment...',
                'required': True,
                'class': 'comment-textarea'  # Optional: Add a CSS class for styling
            }),
        }
