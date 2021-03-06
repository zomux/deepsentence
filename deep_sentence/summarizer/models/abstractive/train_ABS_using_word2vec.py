# -*- coding:utf-8 -*-

import os
import sys
import argparse
import pickle
import time

from gensim.models import Word2Vec
import numpy as np
import pandas as pd
import tensorflow as tf

from models_no_embedding_layer import ABSmodel
import dataset
import id2vector

import config

pd.set_option('display.width', 1000)

parser = argparse.ArgumentParser(description='')
parser.add_argument('--gpu', type=int, default=None)
parser.add_argument('--batch_path', type=str)
parser.add_argument('--w2v_path', type=str)
parser.add_argument('--dictionary_path', type=str)
parser.add_argument('--save_dir', type=str)
args = parser.parse_args()

### dictionaryのload ###
token2id = dataset.load_dictionary(args.dictionary_path)
vocab_size = len(list(token2id.keys()))
id2token = {i:t for t, i in token2id.items()}
config.params.vocab_size = vocab_size
print('vocab size: ', vocab_size)
 
### word2vec ####
print('making id-vector dictionary')
w2v_model = Word2Vec.load_word2vec_format(args.w2v_path, binary=True)
id_vec_dic = id2vector.make_id_vector_dic(w2v_model, id2token, vocab_size)
del w2v_model

### dataのload  ###
print('loading batch')
with open(args.batch_path, 'rb') as f_batch:
    list_batch = pickle.load(f_batch)
 
if args.gpu:
    with tf.device('/gpu:%d'%args.gpu):
        model = ABSmodel(config.params)
        model.build_train_graph()
else:
    model = ABSmodel(config.params)
    model.build_train_graph()

tf.set_random_seed(0)
sess = tf.Session()
sess.run(tf.global_variables_initializer())
# sess.run(tf.initialize_all_variables()) # for lower tf version
save_vals = {'E_w': model.E_w,
             'E_b': model.E_b,
             'F_w': model.F_w,
             'F_b': model.F_b,
             'G_w': model.G_w,
             'G_b': model.G_b,
             'U_w': model.U_w,
             'U_b': model.U_b,
             'V_w': model.V_w,
             'V_b': model.V_b,
             'W_w': model.W_w,
             'W_b': model.W_b,
             'P': model.P}
saver = tf.train.Saver(save_vals)

log_dir = args.save_dir+'/log'
log_path = log_dir+'/train_log.csv'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
with open(log_path, 'w') as f_log:
    f_log.write('epoch,batch,accuracy\n')
    
seed = 0

for i in range(config.params.epoch):
    print('epoch: %d'%(i+1))
    accuracy = 0
    rng = np.random.RandomState(seed) 
    perm = rng.permutation(len(list_batch))
    for j, index in enumerate(perm):
        batch = id2vector.convert_batch(list_batch[index], id_vec_dic)
        sys.stdout.write('\r  batch: %5d (/%5d)'%(j+1, len(list_batch)))
        x = batch['x']
        y_c = batch['y_c'].reshape(config.params.batch_size, -1)
        t_onehot = batch['t_onehot']
        model.train(sess, x, y_c, t_onehot)
        if (j+1) % 5000 == 0: 
            print()
            feed_dict={model.x: x, model.y_c: y_c, model.t: t_onehot}
            accuracy = model.accuracy.eval(session=sess, feed_dict=feed_dict)
            print('  accuracy: %f'%accuracy)
            
            save_dir = args.save_dir+'/epoch%d-batch%d'%(i+1, j+1)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            save_path = saver.save(sess, save_dir+'/model.ckpt')
            print('  Model saved in file: %s' % save_path)
            
            with open(log_path, 'a') as f_log:
                f_log.write('%d,%d,%f\n'%(i+1, j+1, accuracy))

    print()
    feed_dict={model.x: x, model.y_c: y_c, model.t: t_onehot}
    accuracy = model.accuracy.eval(session=sess, feed_dict=feed_dict)
    print('  accuracy: %f'%accuracy)
    
    save_dir = args.save_dir+'/epoch%d-batch%d'%(i+1, j+1)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = saver.save(sess, save_dir+'/model.ckpt')
    print('  Model saved in file: %s' % save_path)
            
    with open(log_path, 'a') as f_log:
        f_log.write('%d,%d,%f\n'%(i+1, j+1, accuracy))
                
    seed += 1
    
