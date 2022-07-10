from django.urls import path
from . import views

app_name = 'budget'

urlpatterns = [
    path('', views.index, name='index'),
    path('app_review/', views.app_review, name='app_review'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('review_list/', views.AppReviewListView.as_view(), name='review_list'),
    path('appreview_update_form/<int:pk>',
         views.ReviewUpdateView.as_view(), name='appreview_update_form'),
    path('delete_review/<int:pk>', views.ReviewDeleteView.as_view()),
    path('vacation_expense/', views.vacation_expense, name='vacation_expense'),
    path('vacation_list/', views.VacationExpenseListView.as_view(),
         name='vacation_list'),
    path('vacationexpense_update_form/<int:pk>',
         views.VacationUpdateView.as_view(), name='vacation_update'),
    path('delete_vacation/<int:pk>', views.VacationExpenseDeleteView.as_view()),
    path('vacationexpense_detail/<int:pk>',
         views.VacationExpenseDetailView.as_view(), name='vacation_detail'),
    path('faq/', views.user_guide, name='faq'),

]
