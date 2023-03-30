#!/usr/bin/env python 
# -*- coding:utf-8 -*
import pickle
import sys
import pandas as pd

from utils.change_column_names import changeToName
from utils.feature_engineering import *
from utils.labels import *
from utils.pipelines import transformation_pipeline
from utils.strategy import changeToOrder

input_path = sys.argv[1]
output_path = sys.argv[2]
model_file = 'model.pkl'

tick_data = pd.read_csv(input_path)
with open(model_file, 'rb') as f:
    model = pickle.load(f)

tick_data = changeToName(tick_data)
tick_data = transformation_pipeline.fit_transform(tick_data)
tick_data_pred = model.predict(tick_data)

tick_data = pd.concat([tick_data['Index',
                                 'StockCode',
                                 'TickTime',
                                 'LatestTransactionPrice'],
                      tick_data_pred)

order_tick = changeToOrder(tick_data)

order_tick.to_csv(output_path, index = False)

