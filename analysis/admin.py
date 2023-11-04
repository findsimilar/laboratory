"""
Admin page for analysis
"""
from django.contrib import admin
from django_find_similar.models import TextToken
from django_find_similar.models.text import Token

# Register your models here.
admin.site.register(TextToken)
admin.site.register(Token)