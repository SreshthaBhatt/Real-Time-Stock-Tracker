from django.urls import path
from .views import *

urlpatterns = [
    path('', stockPicker,name="stock__picker"),
    path('stocktracker/', stockTracker,name="stocktracker"),
]
