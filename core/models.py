"""
Core models
"""
from io import StringIO

import pandas as pd
from django.db import models
from django.utils.functional import cached_property


class TrainingData(models.Model):
    name = models.CharField(max_length=128, unique=True)
    data = models.JSONField()
    total_rating = models.FloatField(blank=True, null=True)
    rating_data = models.JSONField(blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    @cached_property
    def get_dataframe(self) -> pd.DataFrame:
        return pd.read_json(StringIO(self.data), dtype=str)

    @cached_property
    def get_rating_data(self) -> pd.DataFrame:
        if self.rating_data:
            return pd.read_json(StringIO(self.rating_data), dtype=str)

    @property
    def columns_count(self):
        return len(self.get_dataframe.columns)

    @property
    def rows_count(self):
        return len(self.get_dataframe.index)

    def display_dataframe(self):
        dataframe = self.get_dataframe
        return dataframe.head(10)

    def display_rating_data(self):
        dataframe = self.get_rating_data
        if dataframe is not None:
            return dataframe.head(10)
