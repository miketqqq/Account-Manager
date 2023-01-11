from django.urls import path
from . import views

urlpatterns = [
    path('on_load', views.on_load, name="on_load"),
    path('on_close', views.on_close, name="on_close"),
    path('on_click_button', views.on_click_button, name="on_click_button"),
]