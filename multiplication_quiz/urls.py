from django.urls import path
from . import views
from allauth.account.views import SignupView, LoginView

urlpatterns = [
    path('', views.quiz_view, name='quiz'),
    path('generate-question/', views.generate_question_view, name='generate_question'),
    path('get-counters/', views.get_counters_view, name='get_counters'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('about/', views.about_view, name='about'),
]
