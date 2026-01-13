from django import forms
from projects.models import Appeal


class AppealForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com'
        }),
        required=True,
        label='E-poçt'
    )
    cv = forms.FileField(
        widget=forms.FileInput(attrs={
            'accept': '.pdf,.doc,.docx',
            'class': 'form-control'
        }),
        required=True,
        label='CV faylı'
    )

    class Meta:
        model = Appeal
        fields = [
            'email',
            'cv'
        ]
    