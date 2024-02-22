from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput) 

	class Meta:
		model = User
		fields = ['username', 'email']

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password2'] != cd['password']:
			raise forms.ValidationError('Passwords don\'t match.')
		return cd['password2']
