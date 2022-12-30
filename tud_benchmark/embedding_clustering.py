from tensorflow.keras.utils import to_categorical
from sklearn import preprocessing
from sklearn import svm
from sklearn.cluster import KMeans,SpectralClustering
from sklearn.metrics import normalized_mutual_info_score
import numpy as np
import sklearn

def kmeans_batch(data,labels,runs):
    nmis = []
    for i in range(0,runs):
        kmeans = KMeans(n_clusters=20).fit(data)
        nmis.append(normalized_mutual_info_score(labels,kmeans.labels_))
    return np.mean(nmis)

def simple_nn(X,Y,train_split = 0.7):
    # shuffle data and split into train / test
    shuffled = np.arange(len(X))
    np.random.shuffle(shuffled)

    X = X[shuffled]
    Y = Y[shuffled]

    scaler = sklearn.preprocessing.StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    n_train = int(train_split*len(X))
    X_train= X[:n_train]
    X_test = X[n_train:]
    Y_train = Y[:n_train]
    Y_test = Y[n_train:]

    model = tf.keras.Sequential([
        #tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(64, activation='relu',input_shape=X_train.shape[1:]),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(len(np.unique(classes)), activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(X_train, to_categorical(Y_train-1), epochs=10)
    test_loss, test_acc = model.evaluate(X_test,  to_categorical(Y_test-1), verbose=2)
    
    print('\nTest accuracy:', test_acc)
    
    return test_acc

def svm(X,Y,train_split = 0.8, runs = 10, kernel="rbf"):
    accuracies = []
    for i in range(0,runs):
    
        shuffled = np.arange(len(X))
        np.random.shuffle(shuffled)

        X = X[shuffled]
        Y = Y[shuffled]

        scaler = sklearn.preprocessing.StandardScaler()
        scaler.fit(X)
        X = scaler.transform(X)
        n_train = int(train_split*len(X))
        X_train= X[:n_train]
        X_test = X[n_train:]
        Y_train = Y[:n_train]
        Y_test = Y[n_train:]

        svm = sklearn.svm.SVC(kernel=kernel)
        svm.fit(X_train,Y_train)

        acc = svm.score(X_test,Y_test)
        accuracies.append(acc)
    return np.mean(accuracies)

def spectral_clustering_batch(X,classes,affinity='precomputed',n_clusters = 20,runs = 20):
    nmis = []
    for i in range(0,runs):
        clustering = SpectralClustering(n_clusters=n_clusters,
            assign_labels='discretize',
            affinity=affinity,
            random_state=0).fit(X)
        nmi = normalized_mutual_info_score(clustering.labels_,classes)

    return np.mean(nmis)
