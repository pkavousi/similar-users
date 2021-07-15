# Authors: payam.kavousi@gmail.com
"""
This module provides a estimator with fit-predict methods
"""

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.neighbors import NearestNeighbors

from user_similarity_model.config.core import config


class SimilarityModel(BaseEstimator, TransformerMixin):
    """ "This class is used to find the most similar users to a given user
    it follows the format of SKlearn estimators and can be used in a pipeline"""

    def __init__(
        self,
        n_neighbors=config.model_config.n_neighbors,
        algorithm=config.model_config.nearestneighbors_algorithm,
        metric=config.model_config.metric,
    ):

        self.n_neighbors = n_neighbors
        self.algorithm = algorithm
        self.metric = metric
        self.nbrs = NearestNeighbors(
            n_neighbors=self.n_neighbors, algorithm=self.algorithm, metric=self.metric
        )

    def fit(self, X, y=None):
        """fit method uses the transformed dataset to fit a NearestNeighbors model"""
        X = X.set_index("user_handle")
        self.data = X
        self.nbrs.fit(X)
        return self

    def predict(self, user_handler):
        """retuns top similar users to giver user_handle"""
        index = self.nbrs.kneighbors(
            self.data.loc[[user_handler]],
            n_neighbors=self.n_neighbors + 1,
            return_distance=False,
        )
        similar_users = self.data.iloc[index[0]].index.tolist()
        return similar_users[1:]
