from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
username = forms.CharField(max_length=30, help_text="Max length: 30 characters")


from .models import Booking

from django import forms
from .models import Seat, Show

class BookingForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    selected_seats = forms.ModelMultipleChoiceField(
        queryset=Seat.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        show = kwargs.pop('show')
        super().__init__(*args, **kwargs)
        self.fields['selected_seats'].queryset = show.seat_set.filter(is_booked=False)

    def clean_selected_seats(self):
        selected_seats = self.cleaned_data['selected_seats']
        if not selected_seats:
            raise forms.ValidationError("You must select at least one seat.")
        return selected_seats
