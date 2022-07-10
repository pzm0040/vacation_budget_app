from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import ReviewForm, VacationExpenseForm
from .models import AppReview, VacationExpense
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# App Home Page


def index(request):
    # add more here!
    return render(request, 'budget/index.html')


@ login_required
def app_review(request):
    # post --> form contents --> review list
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.reviewer = request.user
            post.save()
            return redirect(reverse('budget:review_list'))

    # Else render form:
    else:
        form = ReviewForm()

    return render(request, 'budget/app_review.html', context={'form': form})


@ login_required
def vacation_expense(request):
    # post --> form contents --> thank you
    if request.method == 'POST':
        form = VacationExpenseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user
            post.save()
            return redirect(reverse('budget:vacation_list'))

    # Else render form:
    else:
        form = VacationExpenseForm()

    return render(request, 'budget/vacation_expense.html', context={'form': form})


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'budget/signup.html'


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = AppReview
    fields = [
        "feedback",
        "star_rating"
    ]
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('budget:review_list')


class AppReviewListView(LoginRequiredMixin, ListView):
    # list all ratings but filter by user currently logged in
    model = AppReview

    def get_queryset(self):
        return AppReview.objects.filter(reviewer=self.request.user).all()


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = AppReview
    success_url = reverse_lazy('budget:review_list')


def thank_you(request):
    return render(request, 'budget/thank_you.html')


# Vacation Views
class VacationExpenseListView(LoginRequiredMixin, ListView):
    # list all vacations but filter by user currently logged in
    model = VacationExpense

    def get_queryset(self):
        return VacationExpense.objects.filter(username=self.request.user).all()


class VacationUpdateView(LoginRequiredMixin, UpdateView):
    model = VacationExpense
    fields = [
        'location', 'number_in_party', 'vacation_start', 'vacation_end', 'amt_saved', 'flight',
        'flight_per_person', 'hotel', 'hotel_per_day', 'food', 'food_pp_pd', 'actvity', 'activity_pp_pd'
    ]
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('budget:vacation_list')


class VacationExpenseDeleteView(LoginRequiredMixin, DeleteView):
    # NOT WORKING
    model = VacationExpense
    success_url = reverse_lazy('budget:vacation_list')


class VacationExpenseDetailView(LoginRequiredMixin, DetailView):
    # RETURN ONLY ONE MODEL ENTRY PK
    # vacationdetail_detail.html
    model = VacationExpense
    # PK --> {{vacationexpense}}


def user_guide(request):
    return render(request, 'budget/faq.html')
