from feature_selection.thePrecisionLasso.models.PrecisionLasso import PrecisionLasso
import numpy as np
import pandas as pd


def lasso2(filecsv):
    df = pd.read_csv(filecsv).dropna(axis=1)
    features_name = df.columns.values.tolist()
    dataset = np.array(df)
    X=dataset[:,1:]
    y=dataset[:,0]
    # Initialize the model
    model = PrecisionLasso()
    # Setup Basic Parameters
    model.setLogisticFlag(False)  # True for Logistic Regression, False for Linear Regression
    model.setLambda(1)  # Set up regularization weight
    model.setLearningRate(1e-6)  # Set up learning rat

    # Setup Advanced Parameters
    model.calculateGamma(X)  # Calculate gamma
    model.fit(X, y)
    result = model.getBeta()

    lasso2_value = [(i, j) for i, j in zip(features_name[1:], result)]
    lasso2_featurees_name_sort_by_value = sorted(lasso2_value, key=lambda x: x[1], reverse=True)  # 由大到小排序
    lasso2_featurees_name_sort = [x[0] for x in lasso2_featurees_name_sort_by_value]
    return lasso2_featurees_name_sort

def run(filecsv):
    lasso2_sort = lasso2(filecsv)
    return lasso2_sort

