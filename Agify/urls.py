from django.urls import path
from . import views

urlpatterns = [
    path("form/", views.predict_form, name="predict_form"),
    path("predict/", views.predict_age, name="predict_age"),
]
