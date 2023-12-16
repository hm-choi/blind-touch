import tensorflow
from keras import backend as K

SHARE_PATH = 'Path of the stored ciphertext from the main server \
             (The client\'s encrypted feature vector is given to the Main server, then the main server stored it in this path.)'
CLUSTERING_2 = 'Path of the cluster2 to save the result which is also used in the Main server'

SAVED_CTXT2 = 'Path of the ctxt2 from the client'

PK_PATH = 'Path of the public key from the client'
GK_PATH = 'Path of the galois key from the client'
RL_PATH = 'Path of the relinearlization key from the client'
FEATURE_MODEL_PATH = 'Path of the feature model from the training'
MODEL_PATH = 'Path of the model  from the training'

CLUSTER_NUM = 2

poly_modulus_degree = 16384
scale_val = poly_modulus_degree//2

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

swish = tensorflow.keras.activations.swish
