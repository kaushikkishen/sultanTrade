import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class Direction(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x, y = None):
        return self

    def transform(self, x, y = None):