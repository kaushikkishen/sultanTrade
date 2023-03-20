from utils.feature_engineering import *
from utils.labels import *
from sklearn.pipeline import Pipeline

transformation_pipeline = Pipeline(steps=[
    ('LimitRatio', LimitRatio()),
    ('WeightedAvgComPriceSpread', WeightedAvgComPriceSpread()),
    ('LatestTransactionPRiceToTickDiffShift1', LatestTransactionPriceToTickDiff(shift=1)),
    ('Spread', Spread()),
    ('RollingComPriceSpreadMean5', RollingComPriceSpreadMean(window=5)),
    ('RollingComPriceSpreadMean10', RollingComPriceSpreadMean(window=10)),
    ('RollingComPriceSpreadMean15', RollingComPriceSpreadMean(window=15)),
    ('RollingComPriceSpreadMean25', RollingComPriceSpreadMean(window=25)),
    ('RollingComPriceSpreadMean50', RollingComPriceSpreadMean(window=50)),
    ('RollingComPriceSpreadMean100', RollingComPriceSpreadMean(window=100),
    ('RollingTransPriceMean5', RollingTransPriceMean(window=5)),
    ('RollingTransPriceMean10', RollingTransPriceMean(window=10)),
    ('RollingTransPriceMean15', RollingTransPriceMean(window=15)),
    ('RollingTransPriceMean25', RollingTransPriceMean(window=25)),
    ('RollingTransPriceMean50', RollingTransPriceMean(window=50)),
    ('RollingTransPriceMean100', RollingTransPriceMean(window=100)),
    ('TransactionVolume', TransactionVolume())),
    ('RollingComPriceSpreadMeanDiff5', RollingComPriceSpreadMeanDiff(window=5)),
    ('RollingComPriceSpreadMeanDiff10', RollingComPriceSpreadMeanDiff(window=10)),
    ('RollingComPriceSpreadMeanDiff15', RollingComPriceSpreadMeanDiff(window=15)),
    ('RollingComPriceSpreadMeanDiff25', RollingComPriceSpreadMeanDiff(window=25)),
    ('RollingComPriceSpreadMeanDiff50', RollingComPriceSpreadMeanDiff(window=50)),
    ('RollingComPriceSpreadMeanDiff100', RollingComPriceSpreadMeanDiff(window=100)),
    ('RollingTransPriceMeanDiff5', RollingTransPriceMeanDiff(window=5)),
    ('RollingTransPriceMeanDiff10', RollingTransPriceMeanDiff(window=10)),
    ('RollingTransPriceMeanDiff15', RollingTransPriceMeanDiff(window=15)),
    ('RollingTransPriceMeanDiff25', RollingTransPriceMeanDiff(window=25))
    ('RollingTransPriceMeanDiff50', RollingTransPriceMeanDiff(window=50)),
    ('RollingTransPriceMeanDiff100', RollingTransPriceMeanDiff(window=100))
])
