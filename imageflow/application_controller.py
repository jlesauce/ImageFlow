import logging
from pathlib import Path
from typing import List

from imageflow.application_model import ApplicationModel

logger = logging.getLogger(__name__)


class ApplicationController:

    def __init__(self, model: ApplicationModel):
        self._model = model

    @staticmethod
    def move_files(files_list: List[Path], raw_folder: Path, destination_path: Path):
        logger.info(f'Move files: {files_list} from {raw_folder} to {destination_path}')
        for file in files_list:
            file.rename(destination_path / file.name)

    def find_common_files(self, folder_a: Path, folder_b: Path) -> List[Path]:
        files_in_a = folder_a.iterdir()
        files_in_b = [self.get_base_name(file) for file in folder_b.iterdir()]

        return [file for file in files_in_a if self.get_base_name(file) in files_in_b]

    @staticmethod
    def get_base_name(file: Path):
        return file.name.split('.')[0]
