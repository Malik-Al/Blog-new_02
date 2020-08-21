from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    email = forms.EmailField(label='Email', required=True)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise ValidationError('User with this email already exists', code='user_email_exists')
        except User.DoesNotExist:
            return email

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email']




class UserChangeForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', required=False)
    birth_date = forms.DateField(label='День рождения', input_formats=['%Y-%m-%d', '%d.%m.%Y'], required=False)

    def get_initial_for_field(self, field, field_name):
        if field_name in self.Meta.profile_fields:
            return getattr(self.instance.profile, field_name)
        return super().get_initial_for_field(field, field_name)

    def save(self, commit=True):
        user = super().save(commit)
        self.save_profile(commit)
        return user

    def save_profile(self, commit=True):
        profile = self.instance.profile
        for field in self.Meta.profile_fields:
            setattr(profile, field, self.cleaned_data[field])

        if not profile.avatar:
            profile.avatar = None

        if commit:
            profile.save()




    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        profile_fields = ['avatar', 'birth_date']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}



class UserChangePasswordForm(forms.ModelForm):
    password = forms.CharField(max_length=100, required=True, label='New Password',
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=100, required=True, label='New Password confirm',
                                       widget=forms.PasswordInput)
    old_password = forms.CharField(max_length=100, required=True, label='Old Password',
                                        widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.instance
        if not user.check_password(old_password):
            raise ValidationError('Invalid password ', code='invalid_password')
        return old_password

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password_confirm']
        if password_1 != password_2:
            raise ValidationError('New Passwords do not match',
                                  code='passwords_do_not_match')
        return self.cleaned_data

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'old_password']








