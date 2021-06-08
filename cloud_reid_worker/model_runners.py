import abc
import enum
import pathlib

import joblib
from sklearn import linear_model as sk_linear_model
from sklearn import pipeline as sk_pipeline

import preprocessors


class Runners(enum.Enum):
    LOGREG = 2
    TF_IDF_LOGREG_JOBLIB = 3


class BaseRunner(abc.ABC):
    files_path: pathlib.Path
    preprocessor: preprocessors.BasePreprocessor

    @staticmethod
    def from_enum(model_kind: Runners,
                  preprocessor: preprocessors.BasePreprocessor,
                  files_path: pathlib.Path) -> 'BaseRunner':
        if model_kind == Runners.LOGREG:
            if isinstance(preprocessor, preprocessors.TfIdfVect):
                return LogregRunner(preprocessor, files_path)
            else:
                raise TypeError(f"Wrong preprocessor for '{LogregRunner}'")

        elif model_kind == Runners.TF_IDF_LOGREG_JOBLIB:
            if isinstance(preprocessor, preprocessors.Empty):
                return TfIdfLogregJoblib(preprocessor, files_path)
            else:
                raise TypeError(f"Wrong preprocessor for '{TfIdfLogregJoblib}'")

        else:
            raise NotImplementedError(f"Unknown enum value for model runner: {model_kind}")

    def __init__(self,
                 preprocessor: preprocessors.BasePreprocessor,
                 files_path: pathlib.Path) -> None:
        self.preprocessor = preprocessor
        self.files_path = files_path

    @abc.abstractmethod
    def run(self, text: str) -> float:
        pass


class TfIdfLogregJoblib(BaseRunner):
    pipe: sk_pipeline.Pipeline

    def __init__(self,
                 preprocessor: preprocessors.Empty,
                 files_path: pathlib.Path) -> None:
        super().__init__(preprocessor, files_path)
        self.pipe = joblib.load(files_path / 'tf-idf-logreg-pipe.joblib')

    def run(self, text: str):
        # output shape (n_samples, n_classes) - [0, 1]
        # take probability of that 0th sample, has 1st class (toxic)
        return self.pipe.predict_proba([text])[0, 1]


class LogregRunner(BaseRunner):
    model: sk_linear_model.SGDClassifier

    def __init__(self,
                 preprocessor: preprocessors.TfIdfVect,
                 files_path: pathlib.Path):
        super().__init__(preprocessor, files_path)
        self.model = joblib.load(files_path / 'model.joblib')

    def run(self, text: str) -> float:
        tranformed = self.preprocessor.transform(text)

        # output shape (n_samples, n_classes) - [0, 1]
        # take probability of that 0th sample, has 1st class (toxic)
        return self.model.predict_proba(tranformed)[0, 1]
