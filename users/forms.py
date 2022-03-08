'''
this file is used to declare form, modify exist form of django
'''

from django import forms
from store.models import CustomUser as User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    # is_active = forms.BooleanField(initial=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# ModelForm is a helper class that lets you create a Form class from a Django model.
# The generated Form class will have a form field for every model field specified,
# in the order specified in the fields attribute.
class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']


# class ProfileUpdateForm(forms.ModelForm):
# 	class Meta:
# 		model = Profile
# 		fields = ['image']


class UserActivateForm(forms.ModelForm):
    email = forms.EmailField()
    activation_code = forms.CharField()

    class Meta:
        model = User
        fields = ['email']
