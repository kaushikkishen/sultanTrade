import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LinearRegression

class LimitRatio(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        x['LimitDownRatio'] = x['OpeningPrice'] / x['LimitDownPrice']
        x['LimitUpRatio'] = x['LimitUpPrice'] / x['OpeningPrice']

        return x


class WeightedAvgComPriceSpread(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        x['WeightedAvgComPriceSpread'] = x['WeightedAverageCommissionedSellingPriceToTick'] - \
                                         x['WeightedAverageCommissionedBuyingPriceToTick']

        return x


class LatestTransactionPriceToTickDiff(BaseEstimator, TransformerMixin):

    def __init__(self, shift=1):
        self.shift = shift

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        prev_price = 'LatestTransactionPriceToTickShift{}Diff'.format(str(self.shift))
        curr_price = 'LatestTransactionPriceToTick'
        x[prev_price] = x.sort_values(['TickTime']) \
                         .groupby('StockCode')[curr_price] \
                         .shift(self.shift)
        
        x[prev_price] = x[curr_price] - x[prev_price]
        
        return x


class Spread(BaseEstimator, TransformerMixin):

    def __init__(self, price_index=1):
        self.price_index = price_index

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        selling_price = 'SellingPrice' + str(self.price_index)
        buying_price = 'BuyingPrice' + str(self.price_index)
        spread = 'Spread' + str(self.price_index)

        x[spread] = x[selling_price] - x[buying_price]

        return x


class RollingComPriceSpreadMean(BaseEstimator, TransformerMixin):

    def __init__(self, window=5):
        self.window = window

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        rolling_com_price = 'RollingComPriceSpreadMean' + str(self.window)

        se_rolling_com_price = x.sort_values(['TickTime']) \
                                .groupby('StockCode')['WeightedAvgComPriceSpread'] \
                                .rolling(self.window).mean()

        x = x.set_index(['StockCode', x.index])
        x[rolling_com_price] = se_rolling_com_price
        x = x.reset_index(level='StockCode')

        return x


class RollingTransPriceMean(BaseEstimator, TransformerMixin):

    def __init__(self, window=5):
        self.window = window

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        rolling_trans_price = 'RollingTransPriceMean' + str(self.window)

        se_rolling_trans_price = x.sort_values(['TickTime']) \
                                  .groupby('StockCode')['LatestTransactionPriceToTick'] \
                                  .rolling(self.window).mean()

        x = x.set_index(['StockCode', x.index])
        x[rolling_trans_price] = se_rolling_trans_price
        x = x.reset_index(level='StockCode')

        return x


class TransactionVolume(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):

        x['TransactionVolume'] = x.sort_values(['TickTime']) \
                                  .groupby('StockCode')['CumulativeTransactionVolumeToTick'] \
                                  .shift(1).fillna(0)

        x['TransactionVolume'] = x['CumulativeTransactionVolumeToTick'] - x['TransactionVolume']

        return x


class RollingTransPriceMeanDiff(BaseEstimator, TransformerMixin):

    def __init__(self, window=5):
        self.window = window

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        rolling_trans_price = 'RollingTransPriceMean' + str(self.window)
        rolling_trans_price_diff = 'RollingTransPriceMeanDiff' + str(self.window)
        x[rolling_trans_price_diff] = x[rolling_trans_price] - x['LatestTransactionPriceToTick']

        return x


class RollingComPriceSpreadMeanDiff(BaseEstimator, TransformerMixin):

    def __init__(self, window=5):
        self.window = window

    def fit(self, x, y=None):
        return self

    def transform(self, x, y=None):
        x = x.copy()

        rolling_com_price = 'RollingComPriceSpreadMean' + str(self.window)
        rolling_com_price_diff = 'RollingComPriceSpreadMeanDiff' + str(self.window)
        x[rolling_com_price_diff] = x[rolling_com_price] - x['WeightedAvgComPriceSpread']

        return x

from statsmodels.regression.rolling import RollingOLS
import statsmodels.api as sm

class NDayRegression(BaseEstimator, TransformerMixin):

    def __init__(self, n=5):
        self.n = n

    def fit(self, x, y=None):
        return self

    def RollingOLSRegression(self, df):
        """
        performs rolling OLS given x and y. outputs regression coefficient
        """

        df = df.reset_index()
        idx = df.index.to_numpy()

        # Create a new column in the dataframe to store the regression values
        _varname_ = f'{self.n}_reg'
        df[_varname_] = np.nan

        # fit OLS model
        y = df['LatestTransactionPriceToTick']
        x = sm.add_constant(df.index)
        model = RollingOLS(y, x, window=self.n, min_nobs=5)
        rolling_reg = model.fit()

        # Store the OLS coefficient in the dataframe
        df.loc[idx, _varname_] = rolling_reg.params['x1']

        df = df.set_index('index')
        return df

    def transform(self, x, y=None):
        x = x.copy()

        x = x.sort_values(['TickTime']) \
            .groupby('StockCode') \
            .apply(lambda l: self.RollingOLSRegression(l))

        return x