from mnist import MNIST
import numpy as np


class FullDataSets(object):
    def __init__(self, train, test, validation):
        self.train = train
        self.test = test
        self.validation = validation


class DataSet(object):
    def __init__(self, images, labels):
        self.images = np.array(images)
        self.images = np.insert(self.images, 0, 1, axis=1)
        self.labels = np.array(labels)

    @property
    def dim(self):
        return self.images.shape[1]

    @property
    def size(self):
        return self.images.shape[0]


def read_data_sets(one_hot=False, directory='mnist'):
    mndata = MNIST(directory)

    train_raw = mndata.load_training()
    # Use the first 20000
    images = train_raw[0][:20000]
    labels = train_raw[1][:20000]
    selection = np.arange(0, len(labels), 10)
    train = DataSet(images=np.delete(images, selection, 0),
                    labels=np.delete(labels, selection, 0))
    validation = DataSet(images=np.array(images)[selection],
                         labels=np.array(labels)[selection])

    test_raw = mndata.load_testing()
    # Use the first 2000
    images = test_raw[0][:2000]
    labels = test_raw[1][:2000]
    test = DataSet(images=images, labels=labels)

    if one_hot:
        for data_set in [train, test, validation]:
            size = len(data_set.labels)
            one_hot_labels = np.zeros((size, 10))
            one_hot_labels[range(size), data_set.labels] = 1
            data_set.labels = one_hot_labels

    return FullDataSets(train=train, test=test, validation=validation)


def read_logistic_data_sets(class_1, class_2, directory='mnist'):
    data_sets = read_data_sets(directory=directory)

    for data_set in [data_sets.train, data_sets.test, data_sets.validation]:
        mask = (data_set.labels == class_1) | (data_set.labels == class_2)
        data_set.images = data_set.images[mask, :]
        data_set.labels = data_set.labels[mask]
        data_set.labels[data_set.labels == class_1] = 1
        data_set.labels[data_set.labels == class_2] = 0

    return data_sets
