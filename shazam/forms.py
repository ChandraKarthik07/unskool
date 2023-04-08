from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
  class Meta:
    model=User
    fields=['name','username','email','password1','password2']

class Roomform(ModelForm):
  class Meta:
    model = Room
    fields = "__all__"   
    exclude=['Host','participants']
    
class updateuser(ModelForm):
  class Meta:
    model = User
    fields=['avatar','name','username','email','bio']