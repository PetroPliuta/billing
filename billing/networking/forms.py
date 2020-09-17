from django import forms
from .models import Router


class RouterForm(forms.ModelForm):
    class Meta:
        model = Router
        fields = '__all__'
        widgets = {
            'secret': forms.PasswordInput(render_value=True),
        }
