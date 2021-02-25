from django import forms
from django.forms import ModelForm
from .models import Korisnici, Predmeti
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class StudentForm(UserCreationForm):
    username = forms.CharField(label="Your Username")
    password1 = forms.CharField(label="Your Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Your Password", widget=forms.PasswordInput)
    email = forms.EmailField(label = "Email Address")
    first_name = forms.CharField(label = "First Name")
    last_name = forms.CharField(label = "Last Name")
    class Meta:
        model = Korisnici
        fields = ['first_name','last_name','username',
        'email', 'status',
         'password1']
    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        forms.errors = None
        if (password1 or password2) and password1 != password2:
           raise forms.ValidationError(
               _("Password Mismatch."),
               code='password_mismatch',)        
        return password1
    def save(self, commit=True):
        user=super(UserCreationForm, self).save(commit=False)
        user.set_password(self.clean_password())
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    email = forms.EmailField(label = "Email")
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Korisnici
        fields = ['email', 'password'] 

class PredmetiForm(forms.ModelForm):
    class Meta:
        model = Predmeti
        fields = '__all__'