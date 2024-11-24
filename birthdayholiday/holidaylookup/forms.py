from django import forms
from django.core.exceptions import ValidationError

class IDCheckForm(forms.Form):
    id_number = forms.CharField(
        label= "South African ID:",
        max_length=13,
        min_length=13,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder':'Enter your 13 digit SAID'
        }),
    )

    def clean_id_number(self):
        id_number = self.cleaned_data['id_number']

        #Ensure that the ID number only contains digits
        if not id_number.isdigit():
            raise forms.ValidationError("The ID number must contain only digits")
        
        #Perform luhn algorithm check
        if not IDCheckForm.luhn_check(id_number):
            raise forms.ValidationError("The ID number is invalid")
        
        return id_number
        
    @staticmethod
    def luhn_check(id_number):
        """
        Validate the ID number using the luhn algorithm
        """

        sum_ = 0
        alternate = False

        # Traverse digits from right to left
        for digit in reversed(id_number):
            d = int(digit)
            if alternate:
                d *= 2
                if d > 9:
                    d -= 9
            sum_ += d

            alternate = not alternate

        return sum_ % 10 == 0
