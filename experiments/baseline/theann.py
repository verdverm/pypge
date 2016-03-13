from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score

import data as DATA

import tensorflow.python.platform
import tensorflow as tf



def run_explicit_loop():
	for problem in DATA.explicit_problems:
		prob,target = problem.split(";")
		df = DATA.read_datafile("explicit", prob)

		cols = [col for col in df.columns if not (col == target or col == "T" or (len(col)>2 and col[:2] == "D_"))]
		ins = df[cols].as_matrix()
		outs = df[target].values    

		print("\n\n", prob, target, ins.shape, outs.shape, "\n=======================\n")

		ann_model(ins,outs, 24,24)


	for problem in DATA.diffeq_problems:
		prob,target = problem.split(";")
		df = DATA.read_datafile("diffeq", prob)

		cols = [col for col in df.columns if not (col == target or col == "T" or (len(col)>2 and col[:2] == "D_"))]
		ins = df[cols].as_matrix()
		outs = df[target].values    

		print("\n\n", prob, target, ins.shape, outs.shape, "\n=======================\n")

		ann_model(ins,outs, 24,24)



def print_model(name, regr, ins, outs):
	print("  ",name,"\n--------------")

	# The mean square error
	yhat = regr.predict(ins)
	print("   Residual:     %g" % np.mean((yhat - outs) ** 2))
	# Explained variance score: 1 is perfect prediction
	r2 = r2_score(outs, yhat)
	print('   R2:           %g' % r2)
	print()


# Create model
def multilayer_perceptron(_X, _weights, _biases):
    layer_1 = tf.nn.relu(tf.add(tf.matmul(_X, _weights['h1']), _biases['b1'])) #Hidden layer with RELU activation
    layer_2 = tf.nn.relu(tf.add(tf.matmul(layer_1, _weights['h2']), _biases['b2'])) #Hidden layer with RELU activation
    return tf.matmul(layer_2, _weights['out']) + _biases['out']
    # layer_3 = tf.nn.relu(tf.add(tf.matmul(layer_2, _weights['h3']), _biases['b3'])) #Hidden layer with RELU activation
    # return tf.matmul(layer_3, _weights['out']) + _biases['out']


def ann_model(ins, outs, n_hidden_1, n_hidden_2):
	outs = outs.reshape(len(outs),1)

	n_input = len(ins[0])
	n_samples = len(outs)

	# tf Graph input
	x = tf.placeholder("float", [n_samples, n_input])
	y = tf.placeholder("float", [n_samples, 1])

	# Store layers weight & bias
	weights = {
	    'h1': tf.Variable(tf.truncated_normal([n_input, n_hidden_1], stddev=0.1)),
	    'h2': tf.Variable(tf.truncated_normal([n_hidden_1, n_hidden_2], stddev=0.1)),
	    'out': tf.Variable(tf.truncated_normal([n_hidden_2, 1], stddev=0.1))
	    # 'h3': tf.Variable(tf.truncated_normal([n_hidden_2, n_hidden_3], stddev=0.1)),
	    # 'out': tf.Variable(tf.truncated_normal([n_hidden_3, 1], stddev=0.1))
	}
	biases = {
	    'b1': tf.Variable(tf.constant(0.1, shape=[n_hidden_1])),
	    'b2': tf.Variable(tf.constant(0.1, shape=[n_hidden_2])),
	    # 'b3': tf.Variable(tf.constant(0.1, shape=[n_hidden_3])),
	    'out': tf.Variable(tf.constant(0.1, shape=[1]))
	}

	# Construct model
	pred = multilayer_perceptron(x, weights, biases)

	## use mean sqr error for cost function
	cost = (tf.pow(y-pred, 2)) 
	accuracy = tf.reduce_mean(cost)

	# construct an optimizer to minimize cost and fit the data
	train_op = tf.train.AdamOptimizer(0.01).minimize(accuracy) 


	sess = tf.Session()

	init = tf.initialize_all_variables()
	sess.run(init)

	NUM_EPOCH = 2501
	DISPLAY = 100

	a_sum = 0

	for epoch in range(NUM_EPOCH):

		sess.run(train_op, feed_dict={x: ins, y: outs})
		# c = sess.run(cost, feed_dict={x: ins, y: outs})
		if epoch % DISPLAY == 0:
			a = sess.run(accuracy, feed_dict={x: ins, y: outs})
			print(epoch, a)

	a = sess.run(accuracy, feed_dict={x: ins, y: outs})
	print("Final: ", a)
	y_hat = sess.run(pred, feed_dict={x: ins, y: outs})
	r2 = r2_score(outs, y_hat)
	print("R2:    ", r2)

run_explicit_loop()

