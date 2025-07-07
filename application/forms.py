from django import forms

class UserForm(forms.Form):
    user_name = forms.CharField(label="Username", max_length=20)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)