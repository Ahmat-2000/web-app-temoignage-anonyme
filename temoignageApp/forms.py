from custom_user.models import User # tables des utilisateurs
from django.contrib.auth.forms import UserCreationForm # pour créer un formulaire dynamiquement
from django.forms import ModelForm
from django import forms
from .models import TemoignesModel
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('email', 'password1', 'password2')

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100,min_length=10)
    name = forms.CharField(max_length=100,min_length=3)
    message = forms.CharField(widget=forms.Textarea,max_length=800)
    sender = forms.EmailField()
  

class temoignageForm(ModelForm):
	class Meta:
		model = TemoignesModel
		# fields = "__all__"
		exclude = ["victime"]

	def clean_agresseur(self):
		agresseur = self.cleaned_data['agresseur']
		if len(agresseur) == 0:
			msg = "Ce champs ne doit pas être vide"
			raise forms.ValidationError(msg)
		if len(agresseur) < 3:
			msg = "Au moins 3 caractères"
			raise forms.ValidationError(msg)
		return agresseur
	def clean_message(self):
		message = self.cleaned_data['message']
		if len(message) == 0 :
			msg = "Ce champs ne doit pas être vide"
			raise forms.ValidationError(msg)
		if len(message) < 30:
			msg = "Au moins 30 caractères"
			raise forms.ValidationError(msg)
		if len(message) > 800:
			msg = "Au plus 800 caractères"
			raise forms.ValidationError(msg)
		return message
	# def clean(self):
	# 	# cleaned_data = super().clean()
	# 	agresseur = self.cleaned_data.get('agresseur','')
	# 	message = self.cleaned_data.get('message','')
	# 	if len(agresseur) < 8:
	# 		msg = "Ce champs ne doit pas être vide"
	# 		raise forms.ValidationError(msg)
	# 	if len(message) < 20 :
	# 		msg = "Ce champs ne doit pas être vide"
	# 		raise forms.ValidationError(msg)
	# 	if len(message) < 20:
	# 		msg = "Ce champs ne doit pas être vide"
	# 		raise forms.ValidationError(msg)
	# 	return self.cleaned_data
	# def save():
	# 	Employee.objects.filter(first_name__startswith='J').count()