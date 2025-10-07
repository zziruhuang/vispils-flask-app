import numpy as np
import pandas as pd
import os
from rdkit import Chem
#from vispils.predict import *

vispils=pd.read_csv("vispils-all.csv")

def search_csv(row, html_cols):
    properties=row[html_cols]
    output = properties.values[0]
    output[1]=f'{10**output[1]:.2f}'
    prediction_text='η = {:.2f} mPas at {} K'.format(float(output[1]), output[2])

    return output, prediction_text

    
def gcnn_predict(int_smis, int_temp):
    int_smis, df_input=process_int(int_smis, int_temp)
    data=assign_g2cnn_descs(df_input)
    df_smis, df_features=get_gcnn_files(data, savepath="./data/data")
    os.system("python -u predict.py \
	            --data_path data/data-smis.csv \
	            --features_path data/data-descs.csv \
	            --checkpoint_path model/ \
	            --save_dir data/ --hidden_size 100 --gpu 1")
    
    row=pd.read_csv("data/Predict.csv")
    properties=row[['Iso SMILES', 'pred_0', 'Temperature']]
    output=list(properties.values[0])+['Pred.']
    output=['','','','','']
    output[1]=f'{np.exp(properties.values[0][1]):.2f}'
    #prediction_text="{} not included in VISPILS!\nPredict eta using trained model.".format(int_smis)
    prediction_text='η = {:.2f} mPas at {} K'.format(float(output[1]), output[2])
    return output, prediction_text