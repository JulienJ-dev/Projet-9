from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['aria-describedby'] = f'id_{field_name}_help'

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)
