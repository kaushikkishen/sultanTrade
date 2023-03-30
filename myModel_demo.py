#!/usr/bin/env python 
# -*- coding:utf-8 -*
import pickle
import sys
import pandas as pd

from utils.change_column_names import changeToName
from utils.feature_engineering import *
from utils.labels import *
from utils.pipelines import transformation_pipeline
from utils.strategy import Strategy

input_path = sys.argv[1]
output_path = sys.argv[2]
model_file = 'model.pkl'
print('Loaded Libraries...')

tick_data = pd.read_csv(input_path)
# with open(model_file, 'rb') as f:
#     model = pickle.load(f)

print('Loaded data and model...')
tick_data = changeToName(tick_data)
tick_data = transformation_pipeline.fit_transform(tick_data)
# tick_data.drop('Label', axis = 1)
print('Transformed data...')
print('Building orders...')
# tick_data_pred = model.predict(tick_data)

# tick_data = pd.concat([tick_data['Index',
#                                  'StockCode',
#                                  'TickTime',
#                                  'LatestTransactionPrice'],
#                       tick_data_pred)
# tick_data['Label']=tick_data_pred

tick_data = tick_data[['Index', 'StockCode', 'TickTime', 'LatestTransactionPriceToTick',
                       'RollingTransPriceMeanDiff5', 'RollingTransPriceMeanDiff100', 'Label']]
order_tick = Strategy().fit_transform(tick_data)

order_tick.to_csv(output_path, index=False)

