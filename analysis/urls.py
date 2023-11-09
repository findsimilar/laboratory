"""
Analysis app urls
"""
from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('tokenize-one/', views.TokenizeOneView.as_view(), name="tokenize_one"),
    path('compare-two/', views.CompareTwoView.as_view(), name="compare_two"),
    path('find-similar/', views.FindSimilarFormView.as_view(), name="find_similar"),
    path('result-list/', views.ResultListView.as_view(), name="result_list"),
    path('result/<int:pk>/', views.ResultDetailView.as_view(), name="result"),
    path('text-token-list/', views.TextTokenListView.as_view(), name="text_token_list"),
    path('text-token/<int:pk>/', views.TextTokenDetailView.as_view(), name="text_token"),
    path('clear-text-token/', views.clear_text_token, name="clear_text_token"),
    path('tokenize/', views.TokenizeView.as_view(), name="tokenize"),
]
