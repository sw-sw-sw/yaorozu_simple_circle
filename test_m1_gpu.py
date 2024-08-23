import tensorflow as tf

with tf.device('/GPU:0'):
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
    c = tf.matmul(a, b)

print(c)
print(c.device)  # '/job:localhost/replica:0/task:0/device:GPU:0' のように表示されるはず