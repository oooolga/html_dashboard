__author__ = "Olga (Ge Ya) Xu"

## The following code follows the tf's MNIST example:
# https://www.tensorflow.org/versions/r0.10/tutorials/mnist/pros/index.html#deep-mnist-for-experts

def load_data():
	from tensorflow.examples.tutorials.mnist import input_data
	mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
	return mnist

def train_model(data, log_dir):
	import tensorflow as tf
	def weight_variable(shape):
		initial = tf.truncated_normal(shape, stddev=0.1)
		return tf.Variable(initial)

	def bias_variable(shape):
		initial = tf.constant(0.1, shape=shape)
		return tf.Variable(initial)

	def conv2d(x, W):
		return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

	def max_pool_2x2(x):
		return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
					strides=[1, 2, 2, 1], padding='SAME')

	sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

	x = tf.placeholder(tf.float32, shape=[None, 784])
	y_ = tf.placeholder(tf.float32, shape=[None, 10])

	W_conv1 = weight_variable([5, 5, 1, 32])
	b_conv1 = bias_variable([32])

	x_image = tf.reshape(x, [-1,28,28,1])

	h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
	h_pool1 = max_pool_2x2(h_conv1)

	W_conv2 = weight_variable([5, 5, 32, 64])
	b_conv2 = bias_variable([64])

	h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
	h_pool2 = max_pool_2x2(h_conv2)

	W_fc1 = weight_variable([7 * 7 * 64, 1024])
	b_fc1 = bias_variable([1024])

	h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
	h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

	keep_prob = tf.placeholder(tf.float32)
	h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

	W_fc2 = weight_variable([1024, 10])
	b_fc2 = bias_variable([10])

	y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

	cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))
	train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
	pred = tf.argmax(y_conv,1)
	label = tf.argmax(y_,1)
	correct_prediction = tf.equal(pred, label)
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

	with sess.as_default():
		sess.run(tf.initialize_all_variables())

		train_acc = []
		train_loss = []
		for i in range(5000):
			batch = data.train.next_batch(50)
			if i%100 == 0:
				train_accuracy, train_pred, train_label, train_cost = sess.run(
					[accuracy, pred, label, cross_entropy],
					feed_dict={
						x:batch[0], y_: batch[1], keep_prob: 1.0}
					)

				print("step %d, training accuracy %g"%(i, train_accuracy))

				if log_dir:
					with open(log_dir, 'ab') as f:
						f.write("step %d, training accuracy %g\n"%(i, train_accuracy))

				train_acc.append(train_accuracy)
				train_loss.append(train_cost)

			train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

		test_accuracy, test_pred, test_label = sess.run(
				[accuracy, pred, label],
				feed_dict={
					x: data.test.images, y_: data.test.labels, keep_prob: 1.0
				}
			)

		print("\ntest accuracy %g"%test_accuracy)

		with open(log_dir, 'ab') as f:
			f.write("\ntest accuracy %g\n"%test_accuracy)

	return {'train_images': batch[0].reshape(50, 28, 28), 
			'train_pred': train_pred, 
			'train_label': train_label,
			'train_acc': train_acc,
			'train_loss': train_loss,
			'test_images': data.test.images.reshape(10000,28,28),
			'test_pred': test_pred,
			'test_label': test_label}


def train_script(demo_folder):
	data = load_data()
	model_results = train_model(data, log_dir='{}/mnist_log.txt'.format(demo_folder))

	return model_results, '{}/mnist_log.txt'.format(demo_folder)

