from django import forms

AMOUNT_PRODUCT = [(i, str(i)) for i in range(1, 10)]


class AmountProductInCart(forms.Form):
    amount = forms.TypedChoiceField(choices=AMOUNT_PRODUCT, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
