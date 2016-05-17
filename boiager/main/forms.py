from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class PwdChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PwdChangeForm, self).__init__(*args, **kwargs)

        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None

