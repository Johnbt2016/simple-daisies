import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
# the data, split between train and test sets
from keras.utils import np_utils
from sklearn.model_selection import KFold
# from tensorflow.python.keras import Sequential
from tensorflow.keras.optimizers import SGD
import matplotlib.pyplot as plt
import numpy as np
# the MNIST data is split between train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()


# Reshape to be samples*pixels*width*height
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1).astype('float32')

# One hot Code
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

# convert from integers to floats
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
# normalize to range [0,1]
X_train = X_train / 255.0
X_test = X_test / 255.0

# Create model
# Building CNN
def create_model():
    model = keras.Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(10, activation='softmax'))
    opt = SGD(learning_rate=0.01, momentum=0.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

    return model

def evaluate_model(n_folds=5):
    accuracy, data = list(), list()
    # prepare 5-cross validation
    kfold = KFold(n_folds, shuffle=True, random_state=1)

    for x_train, x_test in kfold.split(X_train):
        # create model
        model = create_model()
        opt = SGD(learning_rate=0.01, momentum=0.9)
        model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
        # select rows for train and test
        trainX, trainY, testX, testY = X_train[x_train], y_train[x_train], X_train[x_test], y_train[x_test]
        # fit model
        data_fit = model.fit(trainX, trainY, validation_data=(testX, testY), epochs=10, batch_size=200)
        # evaluate model
        _, acc = model.evaluate(testX, testY, verbose=0)
        # stores Accuracy 
        accuracy.append(acc)
        data.append(data_fit)
    model.save("digit_recognition.h5")
    return accuracy, data

def train_model():
    # compile model
    model = create_model()
    
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
    # plt.imshow(X_train[1,:,:,0])
    # plt.show()
    model.fit(X_train, y_train, validation_split=0.2, epochs=12, batch_size=32, callbacks=[early_stop])

    model.save("digit_recognition.h5")



# summarize model performance
def summarize_performance(acc):
    # print summary
    print('Accuracy: mean=%.3f std=%.3f, n=%d' % (np.mean(acc) * 100, np.std(acc) * 100, len(acc)))

    # box and whisker plots of results
    plt.boxplot(acc)
    plt.show()

if __name__ == "__main__":
    train_model()
    # evaluate_model()