import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class Strategy(BaseEstimator, TransformerMixin):

    def __init__(self, shares_bought=0, shares_sold=0, balance=0, avg_price_holding_shares=0, shares=0,
                 rolling_mean_100_thres=50,
                 rolling_mean_5_thres=0.0012, stop_loss_limit=0.97, profit_limit=1.005, cut_off_time=143000000,
                 cut_off_timeb=145000000):

        self.shares_bought = shares_bought
        self.shares_sold = shares_sold
        self.balance = balance
        self.avg_price_holding_shares = avg_price_holding_shares
        self.shares = shares
        self.rolling_mean_100_thres = rolling_mean_100_thres
        self.rolling_mean_5_thres = rolling_mean_5_thres
        self.stop_loss_limit = stop_loss_limit  # 1% stop-loss limit
        self.profit_limit = profit_limit  # 0.5% profit limit
        self.cut_off_time = cut_off_time  # cut-off time to dump stocks if have not finished transactions
        self.cut_off_timeb = cut_off_timeb

    def fit(self, x, y=None):
        return self

    def strategy(self, x):

        shares_bought = self.shares_bought
        shares_sold = self.shares_sold
        balance = self.balance
        avg_price_holding_shares = self.avg_price_holding_shares
        shares = self.shares
        rolling_mean_100_thres = self.rolling_mean_100_thres
        rolling_mean_5_thres = self.rolling_mean_5_thres
        stop_loss_limit = self.stop_loss_limit  # 1% stop-loss limit
        profit_limit = self.profit_limit  # 0.5% profit limit
        cut_off_time = self.cut_off_time  # cut-off time to dump stocks if have not finished transactions
        cut_off_timeb = self.cut_off_timeb

        output = pd.DataFrame(columns=['TickTime', 'symbol', 'BSflag', 'dataIdx', 'volume'])

        final_df_pred_2 = x.copy()
        for index, row in final_df_pred_2.iterrows():

            symbol = row['StockCode']
            BSflag = 'N'
            dataIdx = row['Index']
            volume = 0
            TickTime = row['TickTime']
            buy_sell_flag = None
            # 'Index','StockCode','TickTime','LatestTransactionPriceToTick', 'RollingTransPriceMeanDiff5', 'RollingTransPriceMeanDiff100','Label'
            # Check if we can buy 40, 30, 30 shares
            if buy_sell_flag == None and shares_bought < 100 and row[
                'RollingTransPriceMeanDiff5'] > rolling_mean_5_thres * row['LatestTransactionPriceToTick'] and row[
                'RollingTransPriceMeanDiff100'] > rolling_mean_100_thres and row['Label'] == 1:

                balance -= 10 * row['LatestTransactionPriceToTick']
                avg_price_holding_shares = row['LatestTransactionPriceToTick']
                shares_bought += 10
                shares += 10
                buy_sell_flag = 'B'
                BSflag = 'B'
                volume = 10

            # elif buy_sell_flag == None and shares_bought <= 40 and row['RollingTransPriceMeanDiff5'] > rolling_mean_5_thres and row['RollingTransPriceMeanDiff100'] > rolling_mean_100_thres and row['Label'] == 1:
            #     balance -= 30 * row['LatestTransactionPriceToTick']
            #     avg_price_holding_shares = (avg_price_holding_shares * shares + 30 * row['LatestTransactionPriceToTick']) / (shares + 30)
            #     shares_bought += 30
            #     shares += 30
            #     buy_sell_flag = 'B'
            #     BSflag= 'B'
            #     volume = 30

            # elif buy_sell_flag == None and shares_bought <= 70 and row['RollingTransPriceMeanDiff5'] > rolling_mean_5_thres and row['RollingTransPriceMeanDiff100'] > rolling_mean_100_thres and row['Label'] == 1:
            #     balance -= 30 * row['LatestTransactionPriceToTick']
            #     avg_price_holding_shares = (avg_price_holding_shares * shares + 30 * row['LatestTransactionPriceToTick']) / (shares + 30)
            #     shares_bought += 30
            #     shares += 30
            #     buy_sell_flag = 'B'
            #     BSflag= 'B'
            #     volume = 30

            elif buy_sell_flag == None and shares_sold < 100 and shares_bought > 0 and shares_bought > shares_sold and (
                    row['LatestTransactionPriceToTick'] >= profit_limit * avg_price_holding_shares or row[
                'LatestTransactionPriceToTick'] <= stop_loss_limit * avg_price_holding_shares):
                if shares - 10 == 0:
                    avg_price_holding_shares = 0
                else:
                    avg_price_holding_shares = (avg_price_holding_shares * shares - 10 * row[
                        'LatestTransactionPriceToTick']) / (shares - 10)
                shares_sold += 10
                shares -= 10
                balance += 10 * row['LatestTransactionPriceToTick']  ## no need to code
                buy_sell_flag = 'S'
                BSflag = 'S'
                volume = 10

            # elif buy_sell_flag == None and shares_sold <= 40 and shares_bought >= 70 and (row['LatestTransactionPriceToTick'] >= profit_limit * avg_price_holding_shares or row['LatestTransactionPriceToTick'] <= stop_loss_limit * avg_price_holding_shares):
            #     if shares - 30 == 0:
            #         avg_price_holding_shares = 0
            #     else:
            #         avg_price_holding_shares = (avg_price_holding_shares * shares - 30 * row['LatestTransactionPriceToTick']) / (shares - 30)
            #     shares_sold += 30
            #     shares -= 30
            #     balance += 30 * row['LatestTransactionPriceToTick']
            #     buy_sell_flag = 'S'
            #     BSflag= 'S'
            #     volume = 30

            # elif buy_sell_flag == None and shares_sold <= 70 and shares_bought == 100 and (row['LatestTransactionPriceToTick'] >= profit_limit * avg_price_holding_shares or row['LatestTransactionPriceToTick'] <= stop_loss_limit * avg_price_holding_shares):
            #     if shares - 30 == 0:
            #         avg_price_holding_shares = 0
            #     else:
            #         avg_price_holding_shares = (avg_price_holding_shares * shares - 30 * row['LatestTransactionPriceToTick']) / (shares - 30)
            #     shares_sold += 30
            #     shares -= 30
            #     balance += 30 * row['LatestTransactionPriceToTick']
            #     buy_sell_flag = 'S'
            #     BSflag= 'S'
            #     volume = 30

            # for dumping stocks to meet transaction rules after a certain cut-off time
            elif buy_sell_flag == None and row['TickTime'] > cut_off_time and shares_bought < 100:
                balance -= 10 * row['LatestTransactionPriceToTick']
                avg_price_holding_shares = (avg_price_holding_shares * shares + 10 * row[
                    'LatestTransactionPriceToTick']) / (shares + 10)
                shares += 10
                volume = 10
                shares_bought += 10
                buy_sell_flag = 'B'
                BSflag = 'B'

                # for dumping stocks to meet transaction rules after a certain cut-off time
            elif buy_sell_flag == None and row[
                'TickTime'] > cut_off_time and shares_bought == 100 and shares_sold < 100 and avg_price_holding_shares < \
                    row['LatestTransactionPriceToTick']:
                if shares - 10 == 0:
                    avg_price_holding_shares = 0
                else:
                    avg_price_holding_shares = (avg_price_holding_shares * shares - 10 * row[
                        'LatestTransactionPriceToTick']) / (shares - 10)

                balance += 10 * row['LatestTransactionPriceToTick']
                shares -= 10
                volume = 10
                shares_sold += 10
                BSflag = 'S'
            elif buy_sell_flag == None and row[
                'TickTime'] > cut_off_timeb and shares_bought == 100 and shares_sold < 100:
                if shares - 10 == 0:
                    avg_price_holding_shares = 0
                else:
                    avg_price_holding_shares = (avg_price_holding_shares * shares - 10 * row[
                        'LatestTransactionPriceToTick']) / (shares - 10)

                balance += 10 * row['LatestTransactionPriceToTick']
                shares -= 10
                volume = 10
                shares_sold += 10
                BSflag = 'S'


            else:
                buy_sell_flag = 'N'
                BSflag = 'N'
                volume = 0
            # Check if we can sell 40, 30, 30 shares

            output = output.append({'TickTime': TickTime, 'symbol': symbol, 'BSflag': BSflag,
                                    'dataIdx': dataIdx, 'volume': volume}, ignore_index=True)

        return output

    def transform(self, x, y=None):

        output = pd.DataFrame(columns=['symbol', 'BSflag', 'dataIdx', 'volume', 'TickTime'])

        df = x.copy()
        # final_df_pred_2 = df[['Index','StockCode','TickTime','LatestTransactionPriceToTick', 'RollingTransPriceMeanDiff5', 'RollingTransPriceMeanDiff100','Label']]

        output = df.groupby('StockCode').apply(lambda l: self.strategy(l.sort_values('TickTime', ascending=True)))

        output = output.reset_index(drop=True)

        output = output.sort_values('dataIdx', ascending=True)

        output.drop(['TickTime'], axis=1, inplace=True)

        return output