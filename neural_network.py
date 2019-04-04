import numpy as np
import tensorflow as tf
import math
import TFRecord_operate
import Senten_id_seq
import os

num_steps=100000 #训练的次数
batch_size = 128
num_sampled = 64  # Number of negative examples to sample.


valid_size = 16  # Random set of words to evaluate similarity on.
valid_window = 100  # Only pick dev samples in the head of the distribution.
valid_examples = np.random.choice(valid_window, valid_size, replace=False)


def train_word2vec(TFRecordfile,VOCAB,embedding_size ,vocabulary_size,MODEL_SAVE_PATH,MODEL_NAME):#TFRecord文件，词汇表，词向量的维度
    train_inputs = tf.placeholder(tf.int64, shape=[None])
    train_labels = tf.placeholder(tf.int64, shape=[None, 1])
    valid_dataset = tf.constant(valid_examples, dtype=tf.int64)
    global_step = tf.Variable(0, trainable=False)

    embeddings = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0),name="embedding")
    embed = tf.nn.embedding_lookup(embeddings, train_inputs)
    nce_weights = tf.Variable(
        tf.truncated_normal([vocabulary_size, embedding_size], stddev=1.0 / math.sqrt(embedding_size)))
    nce_biases = tf.Variable(tf.zeros([vocabulary_size]))

    loss = tf.reduce_mean(
        tf.nn.nce_loss(weights=nce_weights,
                       biases=nce_biases,
                       labels=train_labels,
                       inputs=embed,
                       num_sampled=num_sampled,
                       num_classes=vocabulary_size))

    optimizer = tf.train.GradientDescentOptimizer(1.0).minimize(loss,global_step=global_step)

    norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keepdims=True))
    normalized_embeddings = embeddings / norm
    valid_embeddings = tf.nn.embedding_lookup(normalized_embeddings, valid_dataset)
    similarity = tf.matmul(valid_embeddings, normalized_embeddings, transpose_b=True)

    saver = tf.train.Saver()
    batch_input, batch_label = TFRecord_operate.get_tfrecord(TFRecordfile, batch_size)

    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)

        ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
        if (ckpt and ckpt.model_checkpoint_path):
            saver.restore(sess, ckpt.model_checkpoint_path)

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        average_loss = 0

        for i in range(num_steps):
            batch_inputs, batch_labels=sess.run([batch_input, batch_label])

            feed_dict = {train_inputs: batch_inputs, train_labels: batch_labels}
            _, loss_val,step= sess.run([optimizer, loss,global_step], feed_dict=feed_dict)
            average_loss += loss_val


            if (i % 2000 == 0):
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)

                if step > 0:
                    average_loss /= 200
                a = sess.run(embeddings)
                print(a[50][100])
                print('Average loss at step ', step, ': ', average_loss)
                average_loss = 0

            if step % 10000 == 0:

                sim = similarity.eval()
                for i in range(valid_size):
                    valid_word = Senten_id_seq.get_word(VOCAB,i)
                    top_k = 8
                    nearest = (-sim[i, :]).argsort()[1:top_k + 1]
                    log_str = 'Nearest to %s:' % valid_word
                    for k in range(top_k):
                        close_word = Senten_id_seq.get_word(VOCAB,nearest[k])
                        log_str = '%s %s,' % (log_str, close_word)
                    print(log_str)
        final_embeddings = normalized_embeddings.eval()

        coord.request_stop()
        coord.join(threads)

