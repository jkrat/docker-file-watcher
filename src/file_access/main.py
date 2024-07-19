import os
import time
import logging
from typing import Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, PatternMatchingEventHandler
from pathlib import PureWindowsPath


class Event(PatternMatchingEventHandler):

    def __init__(self, patterns=None, logger: Optional[logging.Logger] = None) -> None:
        super().__init__(patterns=patterns)
        self.logger = logger or logging.root
        self.logger.info("Event handler initialized")

    def on_created(self, event: FileSystemEvent) -> None:
        super().on_created(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info("Created %s: %s", what, event.src_path)

        # path = PureWindowsPath(event.src_path)
        # path_without_extension = path.with_suffix('')
        # # while path.suffix:
        # #     path = path.with_suffix('')
        # file_name = path_without_extension.name
        # self.logger.info(file_name)

        # new_file_path = f"/usr/src/nextFiles/{file_name}.txt"

        # self.logger.info("text file saved")

        # if os.path.exists(event.src_path):
        #     os.remove(event.src_path)

        # self.logger.info("audio file deleted")

    def on_deleted(self, event: FileSystemEvent) -> None:
        super().on_deleted(event)

        what = "directory" if event.is_directory else "file"
        self.logger.info("Deleted %s: %s", what, event.src_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("Starting file access service")
    incoming_path = os.getenv('INCOMING_DIR', '/home/containeruser/src/incomingFiles')
    logging.info("incoming path " + incoming_path)
    path = incoming_path
    event_handler = Event(patterns=["*.wav"])
    observer = Observer()
    observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

