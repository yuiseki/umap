from umap import UMAP
from sklearn.datasets import make_blobs
from nose.tools import assert_greater_equal
from nose import SkipTest
import numpy as np

try:
    # works for sklearn>=0.22
    from sklearn.manifold import trustworthiness
except ImportError:
    # this is to comply with requirements (scikit-learn>=0.20)
    # More recent versions of sklearn have exposed trustworthiness
    # in top level module API
    # see: https://github.com/scikit-learn/scikit-learn/pull/15337
    from sklearn.manifold.t_sne import trustworthiness


def test_composite_trustworthiness(nn_data):
    data = nn_data[:50]
    model1 = UMAP(
        n_neighbors=10, min_dist=0.01, random_state=42, n_epochs=50
    ).fit(data)
    model2 = UMAP(
        n_neighbors=30, min_dist=0.01, random_state=42, n_epochs=50,
        init=model1.embedding_
    ).fit(data)
    model3 = model1 * model2
    trust = trustworthiness(data, model3.embedding_, 10)
    assert_greater_equal(
        trust,
        0.82,
        "Insufficiently trustworthy embedding for" "nn dataset: {}".format(trust),
    )
    model4 = model1 + model2
    trust = trustworthiness(data, model4.embedding_, 10)
    assert_greater_equal(
        trust,
        0.82,
        "Insufficiently trustworthy embedding for" "nn dataset: {}".format(trust),
    )

@SkipTest
def test_composite_trustworthiness_random_init(nn_data):
    data = nn_data[:50]
    model1 = UMAP(
        n_neighbors=10, min_dist=0.01, random_state=42, n_epochs=50, init="random",
    ).fit(data)
    model2 = UMAP(
        n_neighbors=30, min_dist=0.01, random_state=42, n_epochs=50, init="random",
    ).fit(data)
    model3 = model1 * model2
    trust = trustworthiness(data, model3.embedding_, 10)
    assert_greater_equal(
        trust,
        0.82,
        "Insufficiently trustworthy embedding for" "nn dataset: {}".format(trust),
    )
    model4 = model1 + model2
    trust = trustworthiness(data, model4.embedding_, 10)
    assert_greater_equal(
        trust,
        0.82,
        "Insufficiently trustworthy embedding for" "nn dataset: {}".format(trust),
    )



def test_composite_trustworthiness_on_iris(iris):
    iris_model1 = UMAP(
        n_neighbors=10, min_dist=0.01, random_state=42, n_epochs=100,
    ).fit(iris.data[:, :2])
    iris_model2 = UMAP(
        n_neighbors=10, min_dist=0.01, random_state=42, n_epochs=100,
    ).fit(iris.data[:, 2:])
    embedding = (iris_model1 + iris_model2).embedding_
    trust = trustworthiness(iris.data, embedding, 10)
    assert_greater_equal(
        trust,
        0.82,
        "Insufficiently trustworthy embedding for" "iris dataset: {}".format(trust),
    )
    embedding = (iris_model1 * iris_model2).embedding_
    trust = trustworthiness(iris.data, embedding, 10)
    assert_greater_equal(
        trust,
        0.82,
        "Insufficiently trustworthy embedding for" "iris dataset: {}".format(trust),
    )
