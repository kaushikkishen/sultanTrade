import numpy as np
import pandas as pd
import os
import argparse

from utils.change_column_names import changeToName
from utils.feature_engineering import LimitRatio, Spread


def main():
    parser = argparse.ArgumentParser(description='Test Run')
    parser.add_argument('--data_url', type=str, default=False,
                        help='mnist dataset path')
    parser.add_argument('--train_url', type=str, default=False,
                        help='mnist model path')

    args = parser.parse_args()

    filename = 'tickdata_20221020.csv'
    outfile = 'tickdata_20221020_trial.csv'

    file_path = os.path.join(args.data_url) #file_name
    outfile_path = os.path.join(args.train_url, outfile)

    print(os.getcwd())

    data = pd.read_csv(file_path)

    data = changeToName(data)
    lr = LimitRatio()
    sp = Spread()

    data = lr.fit_transform(data)
    data = sp.fit_transform(data)

    data.to_csv(outfile_path, index = False)


if __name__ == '__main__':
    main()