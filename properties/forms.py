from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'listing_type', 'property_type',
            'price', 'city', 'address', 'area', 'rooms', 'bathrooms',
            'floor', 'total_floors', 'year_built', 'condition', 'phone',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Taqırıp'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Sıypatlaması'}),
            'listing_type': forms.Select(attrs={'class': 'form-input'}),
            'property_type': forms.Select(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Baha (USD)'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Qala'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Mánzili'}),
            'area': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Maydanı (m²)'}),
            'rooms': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Bólmeler sanı'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Juwınıw bólmeler'}),
            'floor': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Qabat nomeri'}),
            'total_floors': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Jalpı qabatlar'}),
            'year_built': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Qurlǵan jılı'}),
            'condition': forms.Select(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Telefon nomeri'}),
        }


PropertyImageFormSet = forms.inlineformset_factory(
    Property, PropertyImage, fields=['image', 'is_main'], extra=3, can_delete=True
)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Atı'})
    )
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Familiyası'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Elektron pochta'})
    )
    phone = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Telefon nomeri'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Paydalanıwshı atı'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Parol'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Paroldi qayta jazıń'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
