from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Post
from .models import Comment

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise forms.ValidationError("メールアドレスまたはパスワードが正しくありません。")
            except User.DoesNotExist:
                raise forms.ValidationError("メールアドレスまたはパスワードが正しくありません。")
        return cleaned_data

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['picture', 'contents'] 

    def clean(self):
        cleaned_data = super().clean()
        picture = cleaned_data.get("picture")
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content'] 