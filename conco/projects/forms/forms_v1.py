from django import forms
from django.utils.translation import gettext_lazy as _
from projects.models import Appeal


class AppealForm(forms.ModelForm):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Ad Soyad')
        }),
        required=True,
        label=_('Ad Soyad')
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Nümunə: example@email.com')
        }),
        required=True,
        label=_('E-poçt')
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Nümunə: 0501234567')
        }),
        required=True,
        label=_('Mobil Nömrə')
    )
    cv = forms.FileField(
        widget=forms.FileInput(attrs={
            'accept': '.pdf,.doc,.docx',
            'class': 'form-control'
        }),
        required=True,
        label=_('CV faylı')
    )

    class Meta:
        model = Appeal
        fields = [
            'full_name',
            'email',
            'phone_number',
            'cv'
        ]
    