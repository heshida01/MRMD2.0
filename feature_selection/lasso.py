from sklearn.linear_model import Lasso
import pandas as pd
import numpy as np
def lasso(file):
<<<<<<< HEAD
    dataset = pd.read_csv(file,engine='python').dropna(axis=1)
=======
    dataset = pd.read_csv(file).dropna(axis=1)
>>>>>>> 693f4dc7a2f863b47ee6530f5ac9eb12fbe8672b
    features_name = dataset.columns.values.tolist()
    dataset = np.array(dataset)

    X = dataset[:, 1:]
    y = dataset[:, 0]

    lasso = Lasso(alpha=.0001, random_state=1)
    lasso.fit(X, y)
    # print(lasso.coef_)
    ranks = {}
    result = [(x, y) for x, y in zip(features_name[1:], lasso.coef_)]
    result = sorted(result, key=lambda x: abs(x[1]), reverse=True)

    return [x[0] for x in result if abs(x[1])>0.0000000000001]
<<<<<<< HEAD

=======
>>>>>>> 693f4dc7a2f863b47ee6530f5ac9eb12fbe8672b
def run(csvfile,logger):
    logger.info('lasso start...')
    feature_list = lasso(csvfile)

    logger.info('lasso end.')
<<<<<<< HEAD
    return feature_list
#
# filepath =  r'J:\多设备共享\work\MRMD2.0-github\mixfeature_frequency_DBD.csv'
# result = lasso(filepath)
=======
    return feature_list
>>>>>>> 693f4dc7a2f863b47ee6530f5ac9eb12fbe8672b
