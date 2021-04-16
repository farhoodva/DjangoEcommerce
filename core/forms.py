from django import forms

# choices = []
# for i in range(1, 31):
#     choices += str(i),


class AddToCartForm(forms.Form):
    item_quantity = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control rounded text-small',
            }))
    # item_quantity = forms.ChoiceField(choices=zip(choices,choices), widget=forms.Select(attrs={
    #     'class': 'form-control  text-small',
    #         }))

