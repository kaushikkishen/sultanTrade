import numpy as np
import pandas as pd
#abcd
from sklearn.base import BaseEstimator, TransformerMixin


class Direction(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x, y = None):
        return self

    def transform(self, x, y = None):

        if x > 0:
            return 1
        if x < 0:
            return -1
        else:
            return 0
