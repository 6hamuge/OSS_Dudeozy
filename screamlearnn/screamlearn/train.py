import feat_extract
from feat_extract import *
import time
import argparse
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D, GlobalAveragePooling1D, MaxPooling1D
import os
import os.path as op
from sklearn.model_selection import train_test_split

def train(args):
    if not op.exists('data/feat.npy') or not op.exists('data/label.npy'):
        if input('No feature/labels found. Run feat_extract.py first? (Y/n)').lower() in ['y', 'yes', '']:
            feat_extract.main()
            train(args)
    else:
        X = np.load('data/feat.npy')
        y = np.load('data/label.npy').ravel()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=233)
    class_count = len(next(os.walk('data/'))[1])

    model = Sequential()
    model.add(Conv1D(64, 3, activation='relu', input_shape=(193, 1)))
    model.add(Conv1D(64, 3, activation='relu'))
    model.add(MaxPooling1D(3))
    model.add(Conv1D(128, 3, activation='relu'))
    model.add(Conv1D(128, 3, activation='relu'))
    model.add(GlobalAveragePooling1D())
    model.add(Dropout(0.5))
    model.add(Dense(class_count, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    y_train = keras.utils.to_categorical(y_train, num_classes=class_count)
    y_test = keras.utils.to_categorical(y_test, num_classes=class_count)

    X_train = np.expand_dims(X_train, axis=2)
    X_test = np.expand_dims(X_test, axis=2)

    start = time.time()
    model.fit(X_train, y_train, batch_size=args.batch_size, epochs=args.epochs)
    score, acc = model.evaluate(X_test, y_test, batch_size=16)

    print('Test score:', score)
    print('Test accuracy:', acc)
    print('Training took: %d seconds' % int(time.time() - start))
    model.save(args.model)

def main(args):
    if args.train:
        train(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--train', action='store_true', help='train neural network with extracted features')
    parser.add_argument('-m', '--model', metavar='path', default='trained_model.h5', help='use this model path on train and predict operations')
    parser.add_argument('-e', '--epochs', metavar='N', default=500, help='epochs to train', type=int)
    parser.add_argument('-b', '--batch-size', metavar='size', default=64, help='batch size', type=int)
    args = parser.parse_args()
    main(args)
