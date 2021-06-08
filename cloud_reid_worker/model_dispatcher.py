import pathlib

import deep_moderator_common.gcloud as gcloud_utils
import model_runners
import preprocessors


class ModelDispatcher:
    def __init__(self, local_base_path: pathlib.Path, remote_base_path: pathlib.PurePosixPath, bucket_name: str):
        self._remote_base_path = remote_base_path
        self._local_base_path = local_base_path
        self._bucket_name = bucket_name
        # maps {community_id -> relative_path}
        self._models_info = {}
        # maps {community_id ->
        #      (model_runners.BaseRunner, preprocessors.BasePreprocessor)}
        self._models = {}

    def _model_reload_required(
            self,
            group_id: int,
            relative_path: pathlib.Path) -> bool:

        if group_id in self._models_info:
            if relative_path == self._models_info[group_id]:
                # hotswap or initialization is not required
                return False
        return True

    def get_model(
            self,
            group_id: int,
            model_kind: model_runners.Runners,
            preprocessor_kind: preprocessors.Preprocessors,
            relative_path: pathlib.Path) -> model_runners.BaseRunner:
        if relative_path.is_absolute():
            raise ValueError("Path should be relative")

        if not self._model_reload_required(group_id, relative_path):
            return self._models[group_id]

        local_full_path = self._local_base_path / relative_path
        if not local_full_path.exists():
            local_full_path.mkdir(parents=True)

        remote_full_path = self._remote_base_path / relative_path

        # pull model from storage
        gstorage = gcloud_utils.GStorageWrapper()
        gstorage.download_folder(self._bucket_name, remote_full_path, local_full_path)

        # make hotswap
        # create a model and write new model to dispatch dictionary

        preprocessor = preprocessors.BasePreprocessor.from_enum(preprocessor_kind, local_full_path)
        model = model_runners.BaseRunner.from_enum(model_kind, preprocessor, local_full_path)

        self._models_info[group_id] = relative_path
        self._models[group_id] = model
        return model
