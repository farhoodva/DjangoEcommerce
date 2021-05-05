from django import forms
from .models import Reviews
# choices = []
# for i in range(1, 31):
#     choices += str(i),

ratings = [
    ('5', '5'),
    ('4', '4'),
    ('3', '3'),
    ('2', '2'),
    ('1', '1'),
]
exp_choices = [
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not sure', 'Not sure'),
]


class AddToCartForm(forms.Form):
    item_quantity = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control rounded text-small',
            }))
    # item_quantity = forms.ChoiceField(choices=zip(choices,choices), widget=forms.Select(attrs={
    #     'class': 'form-control  text-small',
    #         }))


class AddReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=ratings, required=True)
    positive_exp = forms.ChoiceField(choices=exp_choices, required=True)

    class Meta:
        model = Reviews
        fields = ['review',]
        widgets = {
            'review': forms.Textarea(attrs={
                'placeholder': "Type your review",
                'class': 'form-control no-border',
                'required': True,
                'rows': 4
            }),
            'rating': forms.RadioSelect(choices=ratings, attrs={
                    'class': 'form-check'
                    }),

            'positive_exp': forms.RadioSelect(choices=exp_choices, attrs={
                'class': 'form-check',
            })

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review'].required = True
        self.fields['rating'].required = True
