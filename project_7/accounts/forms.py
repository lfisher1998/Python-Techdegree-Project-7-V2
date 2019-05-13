from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.forms.widgets import PasswordInput
from django.contrib.auth.hashers import check_password
from .models import Profile


class UserRegisterForm(UserCreationForm):
    # Form for registering account
    email = forms.EmailField()
    confirm_email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    
    
    
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'confirm_email',
            'password1',
            'password2',
            
        ]
        
        
    def clean(self, *args, **kwargs):
        # check emails match
        email = self.cleaned_data['email']
        confirm_email = self.cleaned_data['confirm_email']
        if email != confirm_email:
            raise ValidationError("Emails must match!")
            
        return super(UserRegisterForm, self).clean(*args, **kwargs)
        
        
class UserUpdateForm(forms.ModelForm):
    # update user info such as username, first name, last name, email
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
    
        
class ProfileUpdateForm(forms.ModelForm):
    # update profile with bio, date of birth, and image
    bio = forms.CharField(max_length=140, label='Biography',
                    widget=forms.Textarea(attrs={'rows': 6}), min_length=10)
    dob = forms.DateField(
        label="Date of birth Ex.('2006-10-25', '10/25/2006', '25/10/06')",
        input_formats = ['%Y-%m-%d',      # '2006-10-25'
                         '%m/%d/%Y',      # '10/25/2006'
                         '%d/%m/%y']      # '25/10/06'
    )
    
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'dob']
        
        
    def clean_bio(self, *args, **kwargs):
        bio = self.cleaned_data['bio']
        if len(bio) < 10:
            raise ValidationError("Your bio must be at least 10 characters long!")
        return bio
    
    
class PasswordChangeCustomForm(PasswordChangeForm):
    # update password and validate using custom validators
    new_password1 = forms.CharField(
        label='New Password',
        widget=PasswordInput(render_value=True)
    )
    
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=PasswordInput(render_value=True)
    )
    
    class Meta:
        fields = ['new_password1', 'new_password2']
        
        
    def clean(self, *args, **kwargs):
        user = self.user
        new_password = self.cleaned_data.get('new_password1')
        old_password = self.cleaned_data.get('old_password')
        
        
        if new_password == old_password:
            raise forms.ValidationError(
                "New password cannot match the old password.")
            
        user_first_name = user.first_name.lower()
        user_last_name = user.last_name.lower()
        user_username = user.username.lower()

        if (user_first_name in new_password.lower() or user_last_name in
          new_password.lower() or user_username in new_password.lower()):
            raise ValidationError("The new password cannot contain your "
                "username ({}) or parts of your full name ({} {}).".format(
                    user.username, user.first_name, user.last_name))

        return self.cleaned_data
        
        
        

    