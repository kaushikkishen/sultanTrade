import numpy as np
import pandas as pd
import os
import argparse
import pickle

from utils.change_column_names import changeToName
from utils.feature_engineering import *
from utils.labels import *
from utils.data_loader import train_files, test_files, all_files
from utils.pipelines import transformation_pipeline

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser(description='Test Run')
    parser.add_argument('--data_url', type=str, default=False,
                        help='mnist dataset path')
    parser.add_argument('--train_url', type=str, default=False,
                        help='mnist model path')

    args = parser.parse_args()

    for file in train_files:

        file_path = os.path.join(args.data_url, file)
        this_data = pd.read_csv(file_path)
        this_data = changeToName(this_data)
        this_data = transformation_pipeline.fit_transform(this_data)

        if train_files.index(file) == 0:
            all_data = this_data
        else:
            all_data = pd.concat([all_data, this_data])

    X = all_data.drop('Label', axis=1)
    y = all_data['Label']

    model = Pipeline(steps=[
        ('OneHotEncode', OneHotEncoder()),
        ('Classifier', RandomForestClassifier())
        ])

    model.fit(X, y)

    with open(os.path.join(args.train_url, 'TransformationPipeline.pkl'), 'wb') as f:
        pickle.dump(transformation_pipeline, f)

    with open(os.path.join(args.train_url, 'RandomForestModelRun1.pkl'), 'wb') as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    main()