import numpy as np
import random
from utils import ModelUtils

empty_vector = []
for i in range(0, 100):
    empty_vector.append(float(0.0))
onevector = []
for i in range(0, 10):
    onevector.append(float(1))
zerovector = []
for i in range(0, 10):
    zerovector.append(float(0))

def build_vocab():

    vocab = set()

    for line in open('trainingset1'):
        items = line.strip().split(' ')
        for i in range(2, 4):
            words = items[i].split('_')
            vocab.update(words)
    for line in open('dev6'):
        items = line.strip().split(' ')
        for i in range(2, 4):
            words = items[i].split('_')
            vocab.update(words)

    return vocab

def rand_qa(qalist):
    index = random.randint(0, len(qalist) - 1)
    return qalist[index]

def read_alist():
    alist = []
    for line in open('trainingset1'):
        items = line.strip().split(' ')
        alist.append(items[3])
    return alist

def vocab_plus_overlap(vectors, sent, over, size):
    global onevector
    global zerovector
    oldict = {}
    words = over.split('_')
    if len(words) < size:
        size = len(words)
    for i in range(0, size):
        if words[i] == '<a>':
            continue
        oldict[words[i]] = '#'
    matrix = []
    words = sent.split('_')
    if len(words) < size:
        size = len(words)
    for i in range(0, size):
        vec = read_vector(vectors, words[i])
        newvec = vec.copy()
        matrix.append(newvec)
    return matrix

def load_vectors():
    vectors = {}
    for line in open('vectors.nobin'):
        items = line.strip().split(' ')
        if (len(items) < 101):
            continue
        vec = []
        for i in range(1, 101):
            vec.append(float(items[i]))
        vectors[items[0]] = vec
    return vectors

def read_vector(vectors, word):
    global empty_vector
    if word in vectors:
        return vectors[word]
    else:
        return empty_vector
        #return vectors['</s>']

def load_test_and_vectors():
    testList = []
    for line in open('dev6'):
        testList.append(line.strip())
    vectors = load_vectors()
    return testList, vectors

def load_train_and_vectors():
    trainList = []
    for line in open('trainingset1'):
        trainList.append(line.strip())
    vectors = load_vectors()
    return trainList, vectors

def load_data_val_10(testList, vectors, index):
    x_train_1 = []
    x_train_2 = []
    x_train_3 = []
    items = testList[index].split(' ')
    x_train_1.append(vocab_plus_overlap(vectors, items[2], items[3], 200))
    x_train_2.append(vocab_plus_overlap(vectors, items[3], items[2], 200))
    x_train_3.append(vocab_plus_overlap(vectors, items[3], items[2], 200))
    return np.array(x_train_1), np.array(x_train_2), np.array(x_train_3)

def read_raw():
    raw = []
    for line in open('trainingset1'):
        items = line.strip().split(' ')
        if items[0] == '1':
            raw.append(items)
    return raw

def encode_sent(vocab, string, size):
    x = []
    words = string.split('_')
    for i in range(0, 50):# change from 200
        if words[i] in vocab:
            x.append(vocab[words[i]])
        else:
            x.append(vocab['UNKNOWN'])
    return x

def load_data_6(W, alist, raw, size):
    x_train_1 = []
    x_train_2 = []
    x_train_3 = []
    for i in range(0, size):
        items = raw[random.randint(0, len(raw) - 1)]
        nega = rand_qa(alist)
        q_words = items[2].split('_')
        a_words = items[3].split('_')
        neg_words = nega.split('_')
        x_train_1_words = []
        x_train_2_words = []
        x_train_3_words = []
        for i in range(50):
            x_train_1_words.append(ModelUtils.build_text_image(W, q_words[i], padding=1))
            x_train_2_words.append(ModelUtils.build_text_image(W, a_words[i], padding=1))
            x_train_3_words.append(ModelUtils.build_text_image(W, neg_words[i], padding=1))

        x_train_1.append(np.array(x_train_1_words).reshape((50,300)))
        x_train_2.append(np.array(x_train_2_words).reshape((50,300)))
        x_train_3.append(np.array(x_train_3_words).reshape((50,300)))
    return np.array(x_train_1), np.array(x_train_2), np.array(x_train_3)

def load_data_val_6(testList, W, index, batch):
    x_train_1 = []
    x_train_2 = []
    x_train_3 = []
    for i in range(0, batch):
        true_index = index + i
        if (true_index >= len(testList)):
            true_index = len(testList) - 1
        items = testList[true_index].split(' ')
        q_words = items[2].split('_')
        a_words = items[3].split('_')
        x_train_1_words = []
        x_train_2_words = []
        x_train_3_words = []
        for i in range(50):
            x_train_1_words.append(ModelUtils.build_text_image(W, q_words[i], padding=1))
            x_train_2_words.append(ModelUtils.build_text_image(W, a_words[i], padding=1))
            x_train_3_words.append(ModelUtils.build_text_image(W, a_words[i], padding=1))

        x_train_1.append(np.array(x_train_1_words).reshape((50,300)))
        x_train_2.append(np.array(x_train_2_words).reshape((50,300)))
        x_train_3.append(np.array(x_train_3_words).reshape((50,300)))
    return np.array(x_train_1), np.array(x_train_2), np.array(x_train_3)

def load_data_restore(testList, vocab, index, batch):
    x_train_1 = []
    x_train_2 = []
    x_train_3 = []
    for i in range(len(testList)):
        
        items = testList[i].split(' ')
        x_train_1.append(encode_sent(vocab, items[2], 100))
        x_train_2.append(encode_sent(vocab, items[3], 100))
        x_train_3.append(encode_sent(vocab, items[3], 100))
    return np.array(x_train_1), np.array(x_train_2), np.array(x_train_3)

def load_data_9(trainList, vectors, size):
    x_train_1 = []
    x_train_2 = []
    y_train = []
    for i in range(0, size):
        pos = trainList[random.randint(0, len(trainList) - 1)]
        posItems = pos.strip().split(' ')
        x_train_1.append(vocab_plus_overlap(vectors, posItems[2], posItems[3], 200))
        x_train_2.append(vocab_plus_overlap(vectors, posItems[3], posItems[2], 200))
        y_train.append([1, 0])
        neg = trainList[random.randint(0, len(trainList) - 1)]
        negItems = neg.strip().split(' ')
        x_train_1.append(vocab_plus_overlap(vectors, posItems[2], negItems[3], 200))
        x_train_2.append(vocab_plus_overlap(vectors, negItems[3], posItems[2], 200))
        y_train.append([0, 1])
    return np.array(x_train_1), np.array(x_train_2), np.array(y_train)

def load_data_val_9(testList, vectors, index):
    x_train_1 = []
    x_train_2 = []
    items = testList[index].split(' ')
    x_train_1.append(vocab_plus_overlap(vectors, items[2], items[3], 200))
    x_train_2.append(vocab_plus_overlap(vectors, items[3], items[2], 200))
    return np.array(x_train_1), np.array(x_train_2)

def load_data_10(vectors, qalist, raw, size):
    x_train_1 = []
    x_train_2 = []
    x_train_3 = []
    items = raw[random.randint(0, len(raw) - 1)]
    nega = rand_qa(qalist)
    x_train_1.append(vocab_plus_overlap(vectors, items[2], items[3], 200))
    x_train_2.append(vocab_plus_overlap(vectors, items[3], items[2], 200))
    x_train_3.append(vocab_plus_overlap(vectors, nega, items[2], 200))
    return np.array(x_train_1), np.array(x_train_2), np.array(x_train_3)

def load_data_11(vectors, qalist, raw, size):
    x_train_1 = []
    x_train_2 = []
    x_train_3 = []
    items = raw[random.randint(0, len(raw) - 1)]
    nega = rand_qa(qalist)
    x_train_1.append(vocab_plus_overlap(vectors, items[2], items[3], 200))
    x_train_2.append(vocab_plus_overlap(vectors, items[3], items[2], 200))
    x_train_3.append(vocab_plus_overlap(vectors, nega, items[2], 200))
    return np.array(x_train_1), np.array(x_train_2), np.array(x_train_3)

def batch_iter(data, batch_size, num_epochs, shuffle=True):
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(len(data)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]
    
