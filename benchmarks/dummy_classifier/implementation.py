from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier as dclf
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
import os
import json
from ..common.benchmark_wrapper import BenchmarkWrapper


class DummyClassifier(BenchmarkWrapper):
    def __init__(self):
        self.benchmarkName = "DummyClassifier"
        super().__init__(self.benchmarkName)
        self.X_train = []
        self.X_test = []
        self.y_train = []
        self.y_test = []
        self.preset_loc = self.home_dir.joinpath(
            "benchmarks", "dummy_classifier", "presets"
        )

    def setSettings(self):
        pass

    def getPresets(self):
        with open(os.path.join(self.preset_loc, "preset1.json")) as f:
            presetFile = json.load(f)
            self.dataset = presetFile["dataset"]
            self.metrics = presetFile["metrics"]
            self.test_split = presetFile["test_split"]
            self.celery_log.info("Presets loaded")

    def startBenchmark(self):
        self.getPresets()
        print(self.dummyClf())

    def benchmarkStatus():
        # TODO: Communication with celery workers to see if the task is completed.
        pass

    def stopBenchmark():
        # TODO : Figure out stopping the benchmark
        pass

    def extractDataset(self):
        if self.dataset == "iris":
            data, target = load_iris(return_X_y=True)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            data,
            target,
            stratify=target,
            test_size=self.test_split,
            shuffle=True,
            random_state=42,
        )
        self.celery_log.info("Dataset extracted")

    def dummyClf(self) -> dict:
        dummy_clf = dclf(strategy="stratified", random_state=42)
        self.extractDataset()
        dummy_clf.fit(self.X_train, self.y_train)
        y_pred = dummy_clf.predict(self.X_test)
        new_results_dict = {}
        results_dict = {
            "accuracy": accuracy_score(self.y_test, y_pred),
            "recall": recall_score(self.y_test, y_pred, average="weighted"),
            "precision": precision_score(self.y_test, y_pred, average="weighted"),
            "f1_score": f1_score(self.y_test, y_pred, average="weighted"),
        }
        for k, v in results_dict.items():
            if k in self.metrics:
                new_results_dict[k] = v
        self.celery_log.info(f"{results_dict}")
        self.celery_log.info("Training task completed")
        return new_results_dict