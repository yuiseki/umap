from umap import AlignedUMAP
from sklearn.metrics import pairwise_distances
from sklearn.cluster import KMeans
import numpy as np
from nose.tools import assert_greater_equal, assert_raises
from sklearn.metrics import adjusted_rand_score
from numpy.testing import assert_array_almost_equal

# ===============================
# Test AlignedUMAP on sliced iris
# ===============================


def nn_accuracy(true_nn, embd_nn):
    num_correct = 0.0
    for i in range(true_nn.shape[0]):
        num_correct += np.sum(np.in1d(true_nn[i], embd_nn[i]))
    return num_correct / true_nn.size


def test_neighbor_local_neighbor_accuracy(aligned_iris, aligned_iris_model):
    data, target = aligned_iris
    for i, slice in enumerate(data):
        data_dmat = pairwise_distances(slice)
        true_nn = np.argsort(data_dmat, axis=1)[:, :10]
        embd_dmat = pairwise_distances(aligned_iris_model.embeddings_[i])
        embd_nn = np.argsort(embd_dmat, axis=1)[:, :10]
        assert_greater_equal(nn_accuracy(true_nn, embd_nn), 0.65)


def test_local_clustering(aligned_iris, aligned_iris_model):
    data, target = aligned_iris

    embd = aligned_iris_model.embeddings_[1]
    clusters = KMeans(n_clusters=2).fit_predict(embd)
    ari = adjusted_rand_score(target[1], clusters)
    assert_greater_equal(ari, 0.75)

    embd = aligned_iris_model.embeddings_[3]
    clusters = KMeans(n_clusters=2).fit_predict(embd)
    ari = adjusted_rand_score(target[3], clusters)
    assert_greater_equal(ari, 0.40)
