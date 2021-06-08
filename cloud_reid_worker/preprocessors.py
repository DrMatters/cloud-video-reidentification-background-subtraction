import abc
import enum
import pathlib
import typing

import joblib
from scipy.sparse import csr
from sklearn.feature_extraction import text as sk_text


class Preprocessors(enum.Enum):
    EMPTY = 0
    FIX_LEN_WORD = 1  # deprecated (maybe, temporarily)
    TF_IDF = 2


class BasePreprocessor(abc.ABC):
    files_path: pathlib.Path

    @staticmethod
    def from_enum(preprocessor_kind: Preprocessors,
                  files_path: pathlib.Path) -> 'BasePreprocessor':
        if preprocessor_kind == Preprocessors.EMPTY:
            return Empty(files_path)

        elif preprocessor_kind == Preprocessors.TF_IDF:
            return TfIdfVect(files_path)

        else:
            raise NotImplementedError("Unknown enum value for preprocessor")

    def __init__(self, files_path: pathlib.Path):
        self.files_path = files_path

    @abc.abstractmethod
    def transform(self, text: str) -> typing.Any:
        pass


class Empty(BasePreprocessor):
    def __init__(self, files_path: pathlib.Path):
        super().__init__(files_path)

    def transform(self, text: str) -> str:
        return text


class TfIdfVect(BasePreprocessor):
    vectorizer: sk_text.TfidfVectorizer

    def __init__(self, files_path: pathlib.Path):
        super().__init__(files_path)

        self.vectorizer = joblib.load(files_path / 'vectorizer.joblib')

    def transform(self, text: str) -> csr.csr_matrix:
        return self.vectorizer.transform([text])
