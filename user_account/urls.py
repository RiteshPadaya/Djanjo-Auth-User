from django.urls import path
from .views import RegisterView,UserView


urlpatterns = [
    path('account/',RegisterView.as_view()),
    path('all/',UserView.as_view())


]