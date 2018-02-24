from format_data import FormatData
import numpy as np

# Ignore sklearn deprecation warnings.
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

# Classifiers
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC

# Graphing
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit


class TrainingSuite:
    def __init__(self):
        self.X_train, self.X_test, self.y_train, self.y_test, self.labels = FormatData().get_dataset()


    def SGDClassifier(self):
        return SGDClassifier()

    def SVC(self):
        return SVC()

    def accuracy(self, clf):
        """
        Returns float accuracy of prediction.
        """
        return np.mean(self.get_predictions(clf) == self.y_test)

    def get_predictions(self, clf):
        """
        Returns class prediction array of count vectors.
        """
        return clf.predict(self.X_test)

    def train_model(self, estimator):
        print("Training model...")
        estimator.fit(self.X_train, self.y_train)

    def plot(self, n_splits, clf):
        print("Plotting Learning Curve...")
        title = str(clf.__class__)
        cv = ShuffleSplit(n_splits=n_splits, test_size=0.2, random_state=0)
        self.__plot_learning_curve(clf, title, self.X_train + self.X_test, self.y_train + self.y_test, cv=cv)

    def __plot_learning_curve(self, estimator, title, X, y, cv=None, n_jobs=1,
                              train_sizes=np.linspace(.1, 1.0, 5)):
        plt.figure()
        plt.title(title)
        plt.xlabel("Training examples")
        plt.ylabel("Score")
        train_sizes, train_scores, test_scores = learning_curve(
            estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
        plt.grid()
        train_scores_mean = np.mean(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)

        plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
        plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")

        plt.legend(loc="best")
        plt.show()
