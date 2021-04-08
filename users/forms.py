from django import forms
from django.core.exceptions import ValidationError

from .models import UserProfile, City, State


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'address_line1', 'address_line2','email', 'phone_number', 'state', 'city',
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
                    'class': 'form-control ,form-control-lg,  rounded',
                    }),
            'address_line2': forms.TextInput(attrs={
                    'placeholder': 'Address line 2',
                    'class': 'form-control ,form-control-lg,  rounded',
                    }),
            'profile_pic': forms.FileInput(attrs={
                    'placeholder': 'profile_pic',
                    'class': 'form-control ,form-control-lg, rounded',
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

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if len(str(data)) != 11 or str(data).startswith('091'):
            raise ValidationError("wrong cellphone format")