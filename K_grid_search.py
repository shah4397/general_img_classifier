import numpy as np
import visual_bow as bow
from sklearn.cluster import MiniBatchKMeans
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.externals import joblib
import glob
import random
import warnings

def cluster_and_split(img_descs, y, training_idxs, test_idxs, val_idxs, K):
    """Cluster into K clusters, then split into train/test/val"""
    # MiniBatchKMeans annoyingly throws tons of deprecation warnings that fill up the notebook. Ignore them.
    warnings.filterwarnings('ignore')

    X, cluster_model = bow.cluster_features(
        img_descs,
        training_idxs=training_idxs,
        cluster_model=MiniBatchKMeans(n_clusters=K)
    )

    warnings.filterwarnings('default')

    X_train, X_test, X_val, y_train, y_test, y_val = bow.perform_data_split(X, y, training_idxs, test_idxs, val_idxs)

    return X_train, X_test, X_val, y_train, y_test, y_val, cluster_model

def run_svm(X_train, X_test, y_train, y_test, scoring,
    c_vals=[0.1, 1, 5, 10, 75], gamma_vals=[0.5, 0.1, 0.01, 0.0001, 0.00001]):

    param_grid = [
      {'C': c_vals, 'kernel': ['linear']},
      {'C': c_vals, 'gamma': gamma_vals, 'kernel': ['rbf']},
     ]

    svc = GridSearchCV(SVC(), param_grid, n_jobs=-1, scoring=scoring)
    svc.fit(X_train, y_train)
    print 'train score (%s):'%scoring, svc.score(X_train, y_train)
    print 'test score (%s):'%scoring, svc.score(X_test, y_test)

    print svc.best_estimator_

    return svc

def run_ada(X_train, X_test, y_train, y_test, scoring,
    n_estimators=[100, 250, 500, 750], learning_rate=[0.8, 0.9, 1.0, 1.1, 1.2]):

    ada_params={
        'n_estimators':n_estimators,
        'learning_rate':learning_rate
    }

    ada = GridSearchCV(AdaBoostClassifier(), ada_params, n_jobs=-1, scoring=scoring)
    ada.fit(X_train, y_train)

    print 'train score (%s):'%scoring, ada.score(X_train, y_train)
    print 'test score (%s):'%scoring, ada.score(X_test, y_test)
    print ada.best_estimator_

    return ada
