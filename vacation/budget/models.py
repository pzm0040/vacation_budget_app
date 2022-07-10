from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from datetime import date
# Create your models here.


class AppReview(models.Model):
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    feedback = models.CharField(max_length=400)
    star_rating = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5)])

    def __str__(self):
        return f"You previously gave a {self.star_rating} star rating."


class Vacation(models.Model):
    username = models.ForeignKey(User, on_delete=models.PROTECT)
    location = models.CharField(max_length=100, null=True, blank=True)
    budget_active = models.BooleanField(default=True)
    number_in_party = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)], default=1)
    vacation_start = models.DateField(auto_now=False, auto_now_add=False)
    vacation_end = models.DateField(auto_now=False, auto_now_add=False)
    amt_saved = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    last_update = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"User {self.username}'s trip to {self.location}."

    @property
    def number_days(self):
        # number of days on vacation
        dt_difference = self.vacation_end - self.vacation_start
        return dt_difference.days

    @property
    def countdown(self):
        # number of days until vacation start date
        today = date.today()
        countdown_days = self.vacation_start - today
        return countdown_days.days

    @property
    def number_months(self):
        try:
            if self.countdown > 0:
                months = self.countdown/30.5
                return round(months, 1)
            else:
                return 0
        except ValueError:
            return "Error"


class VacationExpense(Vacation):
    flight = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    flight_per_person = models.BooleanField(default=False)
    hotel = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    hotel_per_day = models.BooleanField(default=False)
    food = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    food_pp_pd = models.BooleanField(default=False)
    actvity = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    activity_pp_pd = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username}'s {self.location} Vacation"

    @property
    def total_flight(self):
        if self.flight_per_person:
            total_f_cost = self.flight * self.number_in_party
            f_cost_round = round(total_f_cost)
            return f_cost_round
        elif self.flight > 0:
            total_f_cost = self.flight
            f_cost_round = round(total_f_cost)
            return f_cost_round
        else:
            return 0

    @property
    def total_hotel(self):
        if self.hotel_per_day:
            total_h_cost = self.hotel * self.number_days
            h_cost_round = round(total_h_cost)
            return h_cost_round
        elif self.hotel > 0:
            total_h_cost = self.hotel
            h_cost_round = round(total_h_cost)
            return h_cost_round
        else:
            return 0

    @property
    def total_food(self):
        if self.food_pp_pd:
            total_food_cost = self.food * self.number_in_party * self.number_days
            food_round = round(total_food_cost)
            return food_round
        elif self.food > 0:
            food_round = round(self.food)
            return food_round
        else:
            return 0

    @property
    def total_activity(self):
        if self.activity_pp_pd:
            total_act_cost = self.actvity * self.number_in_party * self.number_days
            act_round = round(total_act_cost)
            return act_round
        elif self.actvity > 0:
            act_round = round(self.activity_pp_pd)
            return act_round
        else:
            return 0

    @property
    def total_vacation_cost(self):
        total_v_cost = self.total_flight + self.total_food + \
            self.total_food + self.total_activity
        return total_v_cost

    @property
    def savings_round(self):
        formatted = round(self.amt_saved)
        return formatted

    @property
    def budget_month(self):
        if self.countdown <= 0:
            return "Vacation in the Past"
        elif self.number_months < 1:
            cost_diff = round(self.total_vacation_cost - self.amt_saved)
            # rounding up to a month if less than a month
            b_per_month = cost_diff
            b_round = round(b_per_month)
            return b_round
        else:
            # vacations more than a month out
            cost_diff = round(self.total_vacation_cost - self.amt_saved)
            b_per_month = cost_diff/self.number_months
            b_round = round(b_per_month)
            return b_round

    @property
    def savings_progress(self):
        if self.amt_saved > 0:
            save_percent = (self.amt_saved / self.total_vacation_cost) * 100
            save_round = round(save_percent)
            return save_round
        else:
            return 0
