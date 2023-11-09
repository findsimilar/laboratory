"""
Analysis app urls
"""
from django.urls import path
from . import views

app_name = 'examples'

urlpatterns = [
    path('example-frequency/', views.ExampleFrequencyAnalysis.as_view(), name="example_frequency"),
    path('list/', views.ExampleList.as_view(), name="example_list"),
]
