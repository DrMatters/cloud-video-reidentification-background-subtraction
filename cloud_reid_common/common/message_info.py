import json
import pathlib

from pydantic import BaseModel


class MessageInfoForWorker(BaseModel):
    preprocessor_kind: str
    model_kind: str
    model_path: str
    text: str
    group_id: int
    id: int

    @staticmethod
    def from_json(json_str):
        return MessageInfoForWorker(**json.loads(json_str))

    def get_model_path_as_pathlib(self):
        return pathlib.Path(self.model_path)

    def get_short_info(self) -> str:
        return f"id: '{self.id}', group_id: '{self.group_id}', text: '{self.text}'"
