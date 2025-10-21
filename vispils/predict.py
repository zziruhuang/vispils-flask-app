# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 19:42:36 2019

@author: SY
"""

import warnings

warnings.filterwarnings('ignore')
import pandas as pd
from chemprop.parsing import parse_train_args, modify_train_args
from chemprop.train import make_predictions


import time

if __name__ == '__main__':
    args = parse_train_args()
    # args.checkpoint_dir = './ckpt'
    
    modify_train_args(args)

    df_smis = pd.read_csv(args.data_path)
    df_features = pd.read_csv(args.features_path[0])
    df = pd.concat([df_smis, df_features], axis=1)

    start_time = time.time()

    pred, smiles = make_predictions(args)
    for i in range(len(pred[0])):
        df[f'pred_{i}'] = [item[i] for item in pred]

    print(f"Saving model predictions to file {args.save_dir + '/predict.csv'}")
    df.to_csv(args.save_dir + '/predict.csv', index=False)


    end_time = time.time()
    print(f"Total prediction time = {end_time-start_time:.5f} s")