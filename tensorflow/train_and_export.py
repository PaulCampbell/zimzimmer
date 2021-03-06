import numpy as np
import tensorflow as tf
from voice_feature_extraction import *
from tensorflow.python.training import saver as tf_saver
from tensorflow.contrib.session_bundle import exporter
import tfdeploy as td

td.setup(tf)

# prepare the training and test data
parent_dir = 'voices'
tr_sub_dirs = ['train']
ts_sub_dirs = ['test']
tr_features, tr_labels = parse_audio_files(parent_dir,tr_sub_dirs)
ts_features, ts_labels = parse_audio_files(parent_dir,ts_sub_dirs)

tr_labels = one_hot_encode(tr_labels)
ts_labels = one_hot_encode(ts_labels)


# Neural net config
training_epochs = 5000
n_dim = tr_features.shape[1]
n_classes = 4 # number of people
n_hidden_units_one = 280
n_hidden_units_two = 300
sd = 1 / np.sqrt(n_dim)
learning_rate = 0.01


# Define placeholders for features and class labels
# Tensorflow is gonna fill these things with data
X = tf.placeholder(tf.float32,[None,n_dim], name="input")
Y = tf.placeholder(tf.float32,[None,n_classes])

# Hidden layers
# 1) tanh layer (hyperbolic tangent function)
W_1 = tf.Variable(tf.random_normal([n_dim,n_hidden_units_one], mean = 0, stddev=sd))
b_1 = tf.Variable(tf.random_normal([n_hidden_units_one], mean = 0, stddev=sd))
h_1 = tf.nn.tanh(tf.matmul(X,W_1) + b_1)

# 2) sigmoid layer (The S shaped one, innit)
W_2 = tf.Variable(tf.random_normal([n_hidden_units_one,n_hidden_units_two], mean = 0, stddev=sd))
b_2 = tf.Variable(tf.random_normal([n_hidden_units_two], mean = 0, stddev=sd))
h_2 = tf.nn.sigmoid(tf.matmul(h_1,W_2) + b_2)

# Output layer - Use a softmax so as we can get a classification out of this thing
# rather that a real number
W = tf.Variable(tf.random_normal([n_hidden_units_two,n_classes], mean = 0, stddev=sd))
b = tf.Variable(tf.random_normal([n_classes], mean = 0, stddev=sd))
y_ = tf.nn.softmax(tf.matmul(h_2,W) + b)
y = tf.argmax(y_,1, name="output")

init = tf.global_variables_initializer()


#  gradient descent optimizer to minimise cost function
cost_function = -tf.reduce_sum(Y * tf.log(y_))
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)

cost_history = np.empty(shape=[1],dtype=float)

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(training_epochs):
        _,cost = sess.run([optimizer,cost_function],feed_dict={X:tr_features,Y:tr_labels})
        cost_history = np.append(cost_history,cost)

    model = td.Model()
    model.add(y, sess)
    model.save("model.pkl")

