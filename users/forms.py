from django import forms
from .models import UserProfile


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'address', 'profile_pic']
        widgets = {
            'firstname': forms.TextInput(attrs={
                    'placeholder': 'Firstname',
                    'class': 'form-control , rounded',
                    }),
            'lastname': forms.TextInput(attrs={
                    'placeholder': 'Lastname',
                    'class': 'form-control , rounded',
                    }),
            'address': forms.Textarea(attrs={
                    'placeholder': 'Address',
                    'class': 'form-control , rounded',
                    }),
            'profile_pic': forms.FileInput(attrs={
                    'placeholder': 'profile_pic',
                    'class': 'form-control , rounded ,',
                    }),

        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # field attrs update
    #     for field in self.fields:
    #         self.fields[field].widget.attrs.update({
    #             'class': 'form-control , rounded ,form-select' ,
    #             'placeholder' : self.fields[field].label
    #                         })
    #         self.fields['profile_pic'].widget.attrs.update({
    #             'class': 'custom-file'
    #         })