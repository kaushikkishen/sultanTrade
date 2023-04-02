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

    def find_local_minima(self, x, n):

        loc_min = x.iloc[argrelextrema(x.LatestTransactionPriceToTick.values, np.less_equal, order=n)[0]][
            'LatestTransactionPriceToTick']
        x['Label'] = loc_min
        return x

    def transform(self, x, y=None):
        # df = x.copy()
        # stockunique = df.StockCode.unique()
        # df_stock = df[df['StockCode'] == stockunique[0]]
        # df_stocka = df_stock.sort_values('TickTime', ascending=True)
        # df_stocka['LocalMinima'] = \
        # df_stocka.iloc[argrelextrema(df_stocka.LatestTransactionPriceToTick.values, np.less_equal, order=self.n)[0]]['LatestTransactionPriceToTick']

        # for i in range(1, len(stockunique)):
        #     stock_code = stockunique[i]
        #     df_stock = df[df['StockCode'] == stock_code]
        #     df_stockb = df_stock.sort_values('TickTime', ascending=True)
        #     df_stockb['LocalMinima'] = \
        #     df_stockb.iloc[argrelextrema(df_stockb.LatestTransactionPriceToTick.values, np.less_equal, order=self.n)[0]]['LatestTransactionPriceToTick']

        #     df_stocka = pd.concat([df_stocka, df_stockb], axis=0)

        df = x.copy()
        df = df.groupby('StockCode').apply(
            lambda l: self.find_local_minima(l.sort_values('TickTime', ascending=True), self.n))

        df['Label'] = np.where(df['Label'] > 0, 1, 0)
        df = df.reset_index(drop=True)

        return df


class LocalMaxima(BaseEstimator, TransformerMixin):

    def __init__(self, n=20):
        self.n = n

    def fit(self, x, y=None):
        return self

    def find_local_maxima(self,x, n):
        loc_min = x.iloc[argrelextrema(x.LatestTransactionPriceToTick.values, np.greater_equal, order=n)[0]]['LatestTransactionPriceToTick']
        x['LocalMaxima'] = loc_min
        return x

    def transform(self, x, y=None):

        # df = x.copy()
        # stockunique = df.StockCode.unique()
        # df_stock = df[df['StockCode'] == stockunique[0]]
        # df_stocka = df_stock.sort_values('TickTime', ascending=True)
        # df_stocka['LocalMaxima'] = \
        # df_stocka.iloc[argrelextrema(df_stocka.LatestTransactionPriceToTick.values, np.greater_equal, order=self.n)[0]]['LatestTransactionPriceToTick']

        # for i in range(1, len(stockunique)):
        #     stock_code = stockunique[i]
        #     df_stock = df[df['StockCode'] == stock_code]
        #     df_stockb = df_stock.sort_values('TickTime', ascending=True)
        #     df_stockb['LocalMinima'] = \
        #     df_stockb.iloc[argrelextrema(df_stockb.LatestTransactionPriceToTick.values, np.greater_equal, order=self.n)[0]]['LatestTransactionPriceToTick']

        #     df_stocka = pd.concat([df_stocka, df_stockb], axis=0)

        df = x.copy()
        df_stocka = df.groupby('StockCode').apply(lambda x: self.find_local_maxima(x.sort_values('TickTime', ascending=True), self.n))
        df_stocka = df_stocka.reset_index(drop=True)


        return df_stocka
