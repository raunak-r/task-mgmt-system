from django import forms

# Imports from models.py
from models import User

class UserForm(forms.ModelForm):
	class Meta:
		#Which model are we going to use
		model = User
		#Which fields should be shown in the form
		fields = ('username', )