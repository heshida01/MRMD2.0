from sklearn.feature_selection import RFE
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

def ref_(file):
    dataset = pd.read_csv(file,engine='python').dropna(axis=1)
    features_name = dataset.columns.values.tolist()
    dataset = np.array(dataset)
    X = dataset[:, 1:]
    y = dataset[:, 0]
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    estimator = LinearSVC()
    selector = RFE(estimator=estimator, n_features_to_select=1)
    selector.fit_transform(X, y)
    result = selector.ranking_
    #print(list(zip(map(lambda x: round(x, 4), selector.ranking_), features_name[1:])))
    #result = sorted(result, key=lambda x: x[1], reverse=True)
    result = sorted(zip(map(lambda x: round(x, 4), selector.ranking_), features_name[1:]))
    return [x[1] for x in result]

def run(csvfile,logger):
    logger.info('ref start...')
    feature_list = ref_(csvfile)
    logger.info('ref end.')
    return feature_list

if __name__ == '__main__':
    res = ref_('../mixfeature_frequency_DBD.csv')
    print(res)