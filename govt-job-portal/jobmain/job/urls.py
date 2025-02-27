from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_listings, name='home'),  # Ensure this is set correctly for your home page
]
