from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django import forms
from .models import contact
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","first_name","last_name","password1","password2"]
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
    
    
class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']
        
             
class ContactForm(forms.ModelForm):
    class Meta:
        model = contact
        fields = "__all__"
        
        
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})