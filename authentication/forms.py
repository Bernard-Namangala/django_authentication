"""
authentication forms
"""

import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.core.validators import EmailValidator, URLValidator
from django.core.exceptions import ValidationError
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form
    """
    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form
    """
    class Meta:
        model = User
        fields = ('email',)



class RegistrationForm(CustomUserCreationForm):
    """
    registration form
    """

    class Meta:
        model = User
        fields = ("email", "password1", "password2", )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class EmailValidationOnForgotPassword(PasswordResetForm):
    """
    form to validate if email exits before sending reset password link
    """
    def clean_email(self):
        """
        function to clean email addess
        """
        email = self.cleaned_data['email']

        #if enters an email which doesnt belong to any account
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "There is no user registered with the specified Email address."
            self.add_error('email', msg)
        return email




# edits
class EditName(forms.Form):
    """
    edit name form
    """
    name = forms.CharField(max_length=255)

    def clean_name(self, *args, **kwargs):
        """
        function to validate name
        """
        name = self.cleaned_data['name']

        #allowed characters in name
        name_regex = re.compile(r"^[A-Za-z\s]{2,40}$")

        if not name_regex.match(name):
            #if user enters invalid characters for name
            raise forms.ValidationError("Name contains invalid characters")

        else:
            #else if user enters correct characters for name
            if len(name) < 2:
                raise forms.ValidationError("Name is too short")

            else:
                if len(name) > 255:
                    raise forms.ValidationError("Name is too long")

            if (len(name.split()) > 3):
                #if the user enters more than 3 names
                 raise forms.ValidationError("Too many names only 3 names allowed")

            elif(len(name.split()) < 2):
                #if user enters only firs name
                 raise forms.ValidationError("Please add your last name")
        return name


class EditEmailForm(forms.Form):
    """
    edit email form
    """
    email = forms.CharField(max_length=2089, widget=forms.EmailInput(attrs={'id': 'email', "placeholder":"Enter your new email"}))

    def clean_email(self, *args, **kwargs):
        """
        function to validate email when editing
        """
        email = self.cleaned_data['email']
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            raise forms.ValidationError("you entered invalid email!!")
        user_with_email = User.objects.filter(email=email)
        if user_with_email:
            raise forms.ValidationError("{}{}".format(email, " is already associated with another account"))
        return email


class EditPassword(forms.Form):
    """
    change password form
    """
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'id': 'password', 'name': 'password'}))
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'id': 'con-password',
                                                                                         'name': 'con-password'}))

    def clean_password(self, *args, **kwargs):
        """
        function to validate password
        """
        password = self.cleaned_data['password']

        #allowed characters in password
        password_regex = re.compile(r"^[\w#@$?!]+$")
        if len(password) < 5:
            raise forms.ValidationError("Password is too short")

        else:
            if len(password) > 50:
                raise forms.ValidationError("Password is too long maximum of 50 characters is allowed")
            
            else:
                if not password_regex.match(password):
                    raise forms.ValidationError("Password contains invalid symbols allowed symbols are #@$?!*")
        return password

    def clean_confirm_password(self, *args, **kwargs):
        """
        function to validate confirmation password
        """
        confirm_password = self.cleaned_data['confirm_password']
        try:
            password = self.cleaned_data['password']

        except KeyError:
            password = ''

        if password:
            if not password == confirm_password:
                raise forms.ValidationError("Passwords do not match")
            
        return confirm_password



class EditPhoneNumberForm(forms.Form):
    """
    edit phone number form
    """
    phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'id': 'phone_number',"placeholder":"Enter your new phone number"}))
    
    def clean_phone(self, *args, **kwargs):
        """
        function to validate phone number
        """
        phone = self.cleaned_data['phone']

        if phone.isdecimal():
            pass

        else:
            raise ValidationError(f"{phone} is not a valid number")
        
        return phone