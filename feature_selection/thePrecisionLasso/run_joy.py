## Basic Setup
# Import basic modules
import numpy as np
# Import the model
from models.PrecisionLasso import PrecisionLasso
# Initialize the data

np.random.seed(1)
X = np.random.random([100, 1000])
y = np.random.random([100])

# Initialize the model
model = PrecisionLasso()
# Setup Basic Parameters
model.setLogisticFlag(False) # True for Logistic Regression, False for Linear Regression
model.setLambda(1) # Set up regularization weight
model.setLearningRate(1e-6) # Set up learning rat


# Setup Advanced Parameters
model.calculateGamma(X) # Calculate gamma

# Run
# model.setLearningRate(1e-6) Multiple runs of the model needs to initialize the learning rate every time
model.fit(X, y)

# Print Result
result = model.getBeta()
print(result)