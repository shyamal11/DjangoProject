from django import forms
from .models import UserDetails
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

class SignUpForm(forms.ModelForm):
   
    class Meta:
        model = UserDetails
        fields = ['Username', 'Email', 'Password']

    def clean_Email(self):
        email = self.cleaned_data.get('Email')
        if UserDetails.objects.filter(Email=email).exists():
            raise ValidationError("A user with that email address already exists.")
        return email

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.Password = make_password(self.cleaned_data["Password"])
        if commit:
            user.save()
        return user
    
    
class LoginForm(forms.Form):
    Username = forms.CharField(max_length=50)
    Password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('Username')
        password = cleaned_data.get('Password')

        if username and password:
            try:
                user = UserDetails.objects.get(Username=username)
                if not user.check_password(password):
                    raise forms.ValidationError("Invalid username or password")
            except UserDetails.DoesNotExist:
                raise forms.ValidationError("Invalid username or password")
            
        
        return cleaned_data
