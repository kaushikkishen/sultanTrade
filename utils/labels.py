import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from scipy.signal import argrelextrema


class Direction(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):

        if x > 0:
            return 1
        if x < 0:
            return -1
        else:
            return 0


class LocalMinima(BaseEstimator, TransformerMixin):

    def __init__(self, n=20):
        self.n = n

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):

        local_minima = argrelextrema(x.values, np.less_equal, order=self.n)[0]['LatestTransactionPriceToTick']
        x['LocalMinima'] = x.iloc[local_minima]['LatestTransactionPriceToTick']

        local_minima_index = np.where(x['LocalMinima'] > 0)[0]

        return x
