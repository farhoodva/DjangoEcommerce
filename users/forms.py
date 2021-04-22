from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfile, City, State
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if len(str(data)) != 11 or not str(data).startswith('091'):
            raise ValidationError("wrong cellphone format")
        return data


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'email', 'phone_number','state', 'city', 'address_line1',
                  'address_line2',
                  'profile_pic']
        widgets = {
            'firstname': forms.TextInput(attrs={
                    'placeholder': 'Firstname',
                    'class': 'form-control ,form-control-lg, rounded',
                    }),
            'lastname': forms.TextInput(attrs={
                    'placeholder': 'Lastname',
                    'class': 'form-control ,form-control-lg, rounded',
                    }),
            'address_line1': forms.TextInput(attrs={
                    'placeholder': 'Address Line 1',
                    'class': 'form-control ,form-control-lg, no-border',
                    }),
            'address_line2': forms.TextInput(attrs={
                    'placeholder': 'Address line 2',
                    'class': 'form-control ,form-control-lg, no-border',
                    }),
            'profile_pic': forms.FileInput(attrs={
                    'placeholder': 'profile_pic',
                    'class': 'form-control, form-control-lg, rounded',
                    }),
            'phone_number': forms.NumberInput(attrs={
                    'placeholder': 'e.g 912********',
                    'class': 'form-control ,form-control-lg, rounded',
                    }),
               }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Example@gmail.com',
            'class': 'form-control ,form-control-lg, rounded',
        })
        self.fields['city'].widget.attrs.update({
            'placeholder': 'City',
            'class': 'form-control ,form-control-lg, rounded',
        })
        self.fields['state'].widget.attrs.update({
            'placeholder': 'State',
            'class': 'form-control ,form-control-lg, rounded',
        })
        self.fields['state'].queryset = State.objects.all()
        self.fields['state'].empty_label = 'Select State'
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = self.data.get('state')
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')

            except (ValueError, TypeError):

                pass
        elif self.instance.pk and self.instance.state:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if len(str(data)) != 11 or not str(data).startswith('091'):
            raise ValidationError("wrong cellphone format")
        return data

payment_choices = (
    ('stripe', 'stripe'),
    ('paypal', 'paypal')
)


class UserBillingEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'email', 'phone_number', 'state', 'city', 'address_line1',
                  'address_line2',
                  'payment_method']
        widgets = {
            'firstname': forms.TextInput( attrs={
                    'placeholder': 'Firstname',
                    'class': 'form-control ,form-control-lg, rounded',
                    }),
            'lastname': forms.TextInput(attrs={
                    'placeholder': 'Lastname',
                    'class': 'form-control ,form-control-lg, rounded',
                    }),
            'address_line1': forms.TextInput(attrs={
                    'placeholder': 'Address Line 1',
                    'class': 'form-control ,form-control-lg, no-border',
                    }),
            'address_line2': forms.TextInput(attrs={
                    'placeholder': 'Address line 2',
                    'class': 'form-control ,form-control-lg, no-border',
                    }),
            'payment_method': forms.RadioSelect(choices=payment_choices, attrs={
                    'class': 'form-select',
                    'required': True
                    }),
            'phone_number': forms.NumberInput(attrs={
                    'placeholder': 'e.g 912********',
                    'class': 'form-control ,form-control-lg, rounded',
                    }),
               }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Example@gmail.com',
            'class': 'form-control ,form-control-lg, rounded',
        })
        self.fields['city'].widget.attrs.update({
            'placeholder': 'City',
            'class': 'form-control ,form-control-lg, rounded',
        })
        self.fields['state'].widget.attrs.update({
            'placeholder': 'State',
            'class': 'form-control ,form-control-lg, rounded',
            'empty_label': ' Select State'
        })
        self.fields['state'].queryset = State.objects.all()
        self.fields['state'].empty_label = 'Select State'
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = self.data.get('state')
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')

            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.state:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if len(str(data)) != 11 or not str(data).startswith('091'):
            raise ValidationError("wrong cellphone format")
        return data
