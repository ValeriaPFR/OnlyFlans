from django import forms
from .models import Client, ContactForm

class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = '__all__'

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label="Nombre")
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ClientForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    class Meta:
        model = Client
        fields = ['name', 'lastname', 'email', 'birth_date', 'address', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")

    def save(self, commit=True):
        client = super().save(commit=False)
        client.set_password(self.cleaned_data['password'])
        if commit:
            client.save()
        return client