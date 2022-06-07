from django.urls import path
from back2normal_app import views

urlpatterns = [
 path('', views.home, name='home')
]
