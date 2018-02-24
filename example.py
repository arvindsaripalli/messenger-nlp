from training_suite import TrainingSuite

if __name__ == "__main__":
    ts = TrainingSuite()

    # Model selection.
    classifier = ts.SGDClassifier()

    # Train classifier.
    ts.train_model(classifier)
    print("Done!\n")

    # View predictions.
    labelled_predictions = [ts.labels[prediction] for prediction in ts.get_predictions(classifier)]
    print("Predictions: {}\n".format(labelled_predictions))

    # View model accuracy.
    print("Model accuracy: {}%\n".format(100 * ts.accuracy(classifier)))

    # View learning curve.
    ts.plot(10, classifier)
