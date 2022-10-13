import warnings
from collections import Counter
warnings.filterwarnings("ignore")
import os
import pandas as pd
import numpy as np
from scipy.io import savemat


def match_function(row, position, dataframe, num_max_rss, m_percent):
    intersect = dataframe.apply(lambda x: list(set(x).intersection(set(row))),axis=1)
    intersect[position] = []
    intersect = list(map(lambda x: list(filter(lambda y: y > 0,x)), intersect))
    match_percent = list(map(lambda x: 0 if (len(x)*100)/num_max_rss < m_percent else (len(x)*100)/num_max_rss, intersect))
    return match_percent

# Descending
def sort_df(df):
    return pd.DataFrame(
        data=df.columns.values[np.argsort(-df.values, axis=1)],
        columns=[i for i in range(df.shape[1])]
    )

# Ascending
def sort_asc_df(df):
    return pd.DataFrame(
        data=df.columns.values[np.argsort(df.values, axis=1)],
        columns=[i for i in range(df.shape[1])]
    )

def clean_dataset(org_x_train=None, org_y_train=None, preprocessed_x_train=None, 
                  threshold=None):

    match_percentage = int(threshold)
    preprocessed_x_train = pd.DataFrame(preprocessed_x_train.values)
    # Determine the average number of RSS values in the dataset
    df_x_train = preprocessed_x_train.copy()
    
    num_max_rss = np.max(df_x_train[df_x_train > 0].count(axis=1))
    
    # Sorting the dataset (Descending)
    sorted_df = np.sort(df_x_train)[:, ::-1]
    sorted_df = pd.DataFrame(np.where(sorted_df > 0, 1, -1))
    temp = sort_df(df_x_train).replace(0, df_x_train.shape[1] + 1)
    temp2 = temp.mul(sorted_df).values
    temp2 = pd.DataFrame(np.where(temp2 < 0, 0, temp2)).iloc[:, 0:int(num_max_rss - 1)]

    # Match percentage
    df_match = pd.DataFrame()
    for i in range(0, temp2.shape[0]):
        df_match[i] = match_function(temp2.iloc[i, :], i, temp2, num_max_rss, match_percentage)

    df_idx = pd.DataFrame(df_match.max(axis=1))
    index_zeros = df_idx.index[df_idx[0] == 0].tolist()

    X_train = pd.DataFrame(org_x_train)
    X_train = X_train.drop(index_zeros)
    y_train = org_y_train.drop(index_zeros)

    return X_train, y_train