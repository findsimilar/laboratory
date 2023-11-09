"""
Analysis app urls
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('load-training-data/', views.LoadTrainingDataView.as_view(), name="load_training_data"),
    path('training-data/<int:pk>/', views.TrainingDataDetailView.as_view(), name="training_data"),
    path('delete-training-data/<int:pk>/', views.TrainingDataDeleteView.as_view(), name="delete_training_data"),
    path('training-data-list/', views.TrainingDataListView.as_view(), name="training_data_list"),
    path('clear-training-data/', views.clear_training_data, name="clear_training_data"),
    path('total-rating-form/<int:pk>/', views.TotalRatingFormView.as_view(), name="total_rating_form"),
    path('rating/<int:pk>/', views.RatingView.as_view(), name="rating"),
]
