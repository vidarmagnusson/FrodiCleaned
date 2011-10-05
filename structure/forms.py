from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.flatpages.models import FlatPage
from structure.models import Menu, Highlight

class FlatPageForm(ModelForm):
	class Meta:
		model = FlatPage

class PartialFlatPageForm(ModelForm):
	class Meta:
		model = FlatPage
		fields = ('title', 'content')

class HighlightForm(ModelForm):
	class Meta:
		model = Highlight
		fields = ('title', 'link', 'pages')
		
class MenuForm(ModelForm):
	class Meta:
		model = Menu

class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

