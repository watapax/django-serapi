from django.urls import path

from api.views import LogInView, LogOutView, LoggedView

urlpatterns = [
    path('login/', LogInView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('logged/', LoggedView.as_view()),
]