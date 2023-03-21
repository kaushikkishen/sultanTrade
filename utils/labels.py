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

        # x = x.copy()
        # local_minima = argrelextrema(x.values, np.less_equal, order=self.n)[0]['LatestTransactionPriceToTick']
        # x['LocalMinima'] = x.iloc[local_minima]['LatestTransactionPriceToTick']
        #
        # local_minima_index = np.where(x['LocalMinima'] > 0)[0]

        df = x.copy()
        stockunique = df.StockCode.unique()
        n = 20
        df_stock = df[df['StockCode'] == stockunique[0]]
        df_stocka = df_stock.sort_values('TickTime', ascending=True)
        df_stocka['Label'] = \
        df_stocka.iloc[argrelextrema(df_stocka.LatestTransactionPriceToTick.values, np.less_equal, order=self.n)[0]]['LatestTransactionPriceToTick']

        for i in range(1, len(stockunique)):
            stock_code = stockunique[i]
            df_stock = df[df['StockCode'] == stock_code]
            df_stockb = df_stock.sort_values('TickTime', ascending=True)
            df_stockb['Label'] = \
            df_stockb.iloc[argrelextrema(df_stockb.LatestTransactionPriceToTick.values, np.less_equal, order=self.n)[0]]['LatestTransactionPriceToTick']
            df_stocka = pd.concat([df_stocka, df_stockb], axis=0)

        df_stocka['Label'] = np.where(df_stocka['Label'] > 0, 1, 0)
        return df_stocka


class LocalMaxima(BaseEstimator, TransformerMixin):

    def __init__(self, n=20):
        self.n = n

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):

        df = x.copy()
        stockunique = df.StockCode.unique()
        n = 20
        df_stock = df[df['StockCode'] == stockunique[0]]
        df_stocka = df_stock.sort_values('TickTime', ascending=True)
        df_stocka['Label'] = \
        df_stocka.iloc[argrelextrema(df_stocka.LatestTransactionPriceToTick.values,
                                     np.greater_equal,
                                     order=self.n)[0]]['LatestTransactionPriceToTick']

        for i in range(1, len(stockunique)):
            stock_code = stockunique[i]
            df_stock = df[df['StockCode'] == stock_code]
            df_stockb = df_stock.sort_values('TickTime', ascending=True)
            df_stockb['Label'] = \
            df_stockb.iloc[argrelextrema(df_stockb.LatestTransactionPriceToTick.values,
                                         np.greater_equal,
                                         order=self.n)[0]]['LatestTransactionPriceToTick']
            df_stocka = pd.concat([df_stocka, df_stockb], axis=0)


        return df_stocka
