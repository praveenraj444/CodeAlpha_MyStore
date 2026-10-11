from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import Review, Profile


# ═══════════════════════════════════════════
# REGISTER FORM
# ═══════════════════════════════════════════
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password (min 8 characters)',
            'class': 'form-input',
        }),
        min_length=8,
        label='Password',
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'class': 'form-input',
        }),
        label='Confirm Password',
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-input',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email address',
                'class': 'form-input',
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('இந்த username ஏற்கனவே use-ல இருக்கு.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('இந்த email ஏற்கனவே register ஆகியிருக்கு.')
        return email

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get('password')
        pwd2 = cleaned.get('password_confirm')

        if pwd and pwd2 and pwd != pwd2:
            raise forms.ValidationError('Passwords ரெண்டும் match ஆகல.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# ═══════════════════════════════════════════
# LOGIN FORM
# ═══════════════════════════════════════════
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-input',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-input',
        })
    )

    # ═══════════════════════════════════════════
# CHECKOUT FORM
# ═══════════════════════════════════════════
class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Full name',
            'class': 'form-input',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-input',
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone number',
            'class': 'form-input',
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Street address, house no., landmark',
            'class': 'form-input',
            'rows': 3,
        })
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'City',
            'class': 'form-input',
        })
    )
    pincode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'placeholder': 'Pincode',
            'class': 'form-input',
        })
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 10:
            raise forms.ValidationError('Valid phone number கொடுங்க (min 10 digits).')
        return phone

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode', '').strip()
        if not pincode.isdigit() or len(pincode) != 6:
            raise forms.ValidationError('Pincode 6 digits-ஆ இருக்கணும்.')
        return pincode

# ═══════════════════════════════════════════
# REVIEW FORM
# ═══════════════════════════════════════════
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=Review.RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-radio'}),
        label='Rating',
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Share your experience...',
            'class': 'form-input',
            'rows': 3,
        }),
        required=False,
        label='Review',
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']

        # ═══════════════════════════════════════════
# PROFILE FORMS
# ═══════════════════════════════════════════
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-input'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'city', 'pincode']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-input'}),
            'address': forms.Textarea(attrs={'placeholder': 'Street address', 'class': 'form-input', 'rows': 3}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-input'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Pincode', 'class': 'form-input'}),
        }

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode', '').strip()
        if pincode and (not pincode.isdigit() or len(pincode) != 6):
            raise forms.ValidationError('Pincode must be exactly 6 digits.')
        return pincode


# ═══════════════════════════════════════════
# PASSWORD CHANGE FORM (with CSS classes)
# ═══════════════════════════════════════════
class StyledPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})