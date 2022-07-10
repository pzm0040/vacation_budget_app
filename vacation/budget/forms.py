#from django import forms
from .models import AppReview, VacationExpense
from django.forms import ModelForm, ValidationError
import datetime


# class DateInput(forms.DateInput):
# input_type = 'date'


# class ReviewForm(forms.Form):
#first_name = forms.CharField(label='First Name', max_length=50)
#email = forms.EmailField(label='Email')
# review = forms.CharField(label='Please write your review here',
# widget=forms.Textarea())
# review_date = forms.DateField(label="review_date",
# widget=DateInput)

# rating class will be int field min value 1 and max value 5

class ReviewForm(ModelForm):
    class Meta:
        model = AppReview
        fields = ['feedback', 'star_rating']

        labels = {
            'feedback': "What do you like? What can we improve?",
            'star_rating': "Rating (1-5 Stars)"
        }


class VacationExpenseForm(ModelForm):
    def clean_vacation_start(self):
        data = self.cleaned_data['vacation_start']

        # confirm vacation start date is not in the past
        if data < datetime.date.today():
            raise ValidationError(
                ('Invalid Date - Departure Date is in the Past'))
        return data

    def clean_vacation_end(self):
        data = self.cleaned_data['vacation_end']

        # confirm vacation end date is not in the past
        if data < datetime.date.today():
            raise ValidationError(
                ('Invalid Date - Return Date is in the Past'))
        return data

    class Meta:
        model = VacationExpense
        fields = ['location', 'number_in_party', 'vacation_start', 'vacation_end', 'amt_saved', 'flight',
                  'flight_per_person', 'hotel', 'hotel_per_day', 'food', 'food_pp_pd', 'actvity', 'activity_pp_pd']
        labels = {'location': "Where to? (Travel Destination)",
                  'number_in_party': ' Number of People Traveling',
                  'vacation_start': 'Departure Date',
                  'vacation_end': 'Return Date',
                  'amt_saved': 'Amount Currently Saved for Vacation ($)',
                  'flight': 'Flight Cost ($)',
                  'flight_per_person': 'Is the Flight Cost Per Person?',
                  'hotel': 'Hotel Cost ($)',
                  'hotel_per_day': 'Is the Hotel Cost Per Day?',
                  'food': 'Food Cost ($)',
                  'food_pp_pd': 'Is the Cost Entered Per Person/Per Day?',
                  'actvity': 'Activity Cost ($)',
                  'activity_pp_pd': 'Is the Cost Entered Per Person/Per Day?'
                  }

# class UserRegisterForm(UserCreationForm):
