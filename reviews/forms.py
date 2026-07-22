from django import forms

from .models import Review, Ticket


class TicketForm(forms.ModelForm):
    """Formulaire de création et de modification d'un billet."""

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'image': 'Image',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
        }


class ReviewForm(forms.ModelForm):
    """Formulaire de création et de modification d'une critique."""

    rating = forms.TypedChoiceField(
        label='Note',
        choices=[(rating, str(rating)) for rating in range(6)],
        coerce=int,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
        labels = {
            'headline': 'Titre',
            'body': 'Commentaire',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 8}),
        }
