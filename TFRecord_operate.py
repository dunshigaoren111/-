import tensorflow as tf
import json
import Input_vec
def write_tfRecord(tfRecordName,datafile,skip_window,num_skips):
    writer=tf.python_io.TFRecordWriter(tfRecordName)
    num_pic=0

    data_list,labels=Input_vec.produce_inputs(datafile,skip_window,num_skips)
    for i in range(len(data_list)):
        input_row=data_list[i]
        label=labels[i]
        example=tf.train.Example(features=tf.train.Features(feature={
                                                                'input_row':tf.train.Feature(int64_list=tf.train.Int64List(value=[input_row])),
                                                                'label':tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
                                                            }))
        writer.write(example.SerializeToString())
        num_pic+=1
        print(num_pic)
    writer.close()

def read_tfRecord(tfRecord_path):
    filename_queue=tf.train.string_input_producer(tfRecord_path)
    reader=tf.TFRecordReader()
    _,serialized_example=reader.read(filename_queue)
    features=tf.parse_single_example(serialized_example,
                                     features={

                                         'input_row':tf.FixedLenFeature([1],tf.int64),
                                         'label': tf.FixedLenFeature([1], tf.int64)
                                     })
    label=tf.cast(features['label'],tf.int64)
    input_row=tf.cast(features['input_row'],tf.int64)
    return input_row,label


def get_tfrecord(tfRecord_path,num):
    # if(isTrain):
    #     tfRecord_path=trainfile
    # else:
    #     tfRecord_path = testfile
    input_row, label = read_tfRecord([tfRecord_path])
    input_row_batch, label_batch = tf.train.shuffle_batch([input_row, label],
                                                          batch_size=num,
                                                          num_threads=1,
                                                          capacity=100,
                                                          min_after_dequeue=50)
    label_batch = tf.reshape(label_batch, [-1, 1])
    input_row_batch=tf.reshape(label_batch, [-1])
    return input_row_batch,label_batch



