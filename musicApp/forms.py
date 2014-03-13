from musicApp.models import User
from django.forms import ModelForm

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ["email","password",'createTime']