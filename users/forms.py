from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Contact


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	contact_info = forms.Field(required=True, label="Contact Information")

	class Meta:
		model = User
		fields = ("username", "email", "contact_info", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
			Contact(user=user, info=self.cleaned_data['contact_info']).save()
		return user
