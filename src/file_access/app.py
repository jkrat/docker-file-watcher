import os
import time
import logging
from typing import Optional
from pathlib import Path
from .pattern_matching import match_file_type

class File_Watcher:

    def __init__(
            self, 
            patterns=None, 
            logger: Optional[logging.Logger] = None
        ) -> None:

        self._patterns = patterns
        self.logger = logger or logging.root
        self.logger.info("File watcher initialized")
        self.wait_new_files(self.directory)

    @property
    def directory(self):
        """
        (Read-only)
        Path to save transcribed files.
        """
        return os.getenv('INCOMING_DIR')
    
    @property
    def new_base_path(self):
        """
        (Read-only)
        path to save transcribed files.
        """
        return os.getenv('NEXT_DIR')
    
    @property
    def patterns(self):
        """
        (Read-only)
        Patterns to allow matching file paths.
        """
        return self._patterns
    
    def wait_new_files(self, directory: str) -> None: 
        previous_files = self.get_file_list(directory)
        while True:
            current_files = self.get_file_list(directory)
            new_files = list(set(current_files) - set(previous_files))
            for new_file in new_files:
                file_path = os.path.join(directory, new_file)
                self.access_file(file_path)
            previous_files = current_files
            time.sleep(5)

    def get_file_list(self, directory: str) -> list: 
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and match_file_type(f, included_patterns=self.patterns)]

    def access_file(self, file_path: str) -> None:
        path = Path(file_path)
        self.logger.info("path: %s", path)

        path_without_extension = path.with_suffix('')
        file_name = path_without_extension.name
        new_file_path = os.path.join(self.new_base_path, f"{file_name}.txt")
        self.logger.info("new file path will be %s", new_file_path)

        with open(new_file_path, "x") as file:
            file.write("Success")

        self.logger.info("text file saved")

        if os.path.exists(path):
            self.logger.info("audio file deleted: %s", path)
            os.remove(path)
        else:
            self.logger.info("path for deletion does not exist: %s", path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    File_Watcher(patterns=["*.wav"]) 
    