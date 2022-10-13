import numpy as np
import pandas as pd

np.random.seed(110)

def data_partition(X_train, y_train, test_data_percent):

    X_train = pd.DataFrame(X_train)
    # Get unique labels
    unique_values = y_train.drop_duplicates()
    floors = np.unique(unique_values.iloc[:, 3])
    buildings = np.unique(unique_values.iloc[:, 4])
    
    indexes = []
    indexes_validation = []
    for bld in buildings:
        for flr in floors:
            selection = unique_values.loc[(unique_values['BUILDINGID'] == bld) & (unique_values['FLOOR'] == flr)]
            unique_index = selection.index
            num_samples_valid = int(np.round(selection.shape[0]*(test_data_percent/100)))
            samples_valid = np.random.choice(unique_index, num_samples_valid, replace=False)
            indexes.extend(samples_valid)

    for idx in indexes:
        ref_row = y_train.loc[idx].copy()
        index_valid = y_train.loc[(y_train['LONGITUDE'] == ref_row['LONGITUDE']) &
                                  (y_train['LATITUDE'] == ref_row['LATITUDE']) &
                                  (y_train['ALTITUDE'] == ref_row['ALTITUDE']) &
                                  (y_train['FLOOR'] == ref_row['FLOOR']) &
                                  (y_train['BUILDINGID'] == ref_row['BUILDINGID'])].index
        indexes_validation.extend(index_valid)

    X_new_validation = X_train.loc[indexes_validation].copy()
    X_new_train = X_train.drop(indexes_validation)
    
    y_new_validation = y_train.loc[indexes_validation].copy()
    y_new_train = y_train.drop(indexes_validation)

    return X_new_train,  y_new_train, X_new_validation, y_new_validation
