import abc
import csv
import logging
from typing import Any, Dict, List


class OutputHandler(abc.ABC):
    @abc.abstractmethod
    def save_to_buffer(self, data: Any):
        pass

    @abc.abstractmethod
    def write_output(self):
        pass


class FileOutputHandler(OutputHandler):
    def __init__(self, *, filename: str):
        self.filename = filename
        self.data: List[str] = []
        logging.debug(f"FileOutputHandler initialized for file: {self.filename}")

    def save_to_buffer(self, data: str):
        self.data.append(data)
        logging.debug(f"Buffered data for file output: {data}")

    def write_output(self):
        try:
            with open(self.filename, "a") as file:
                file.write("\n".join(self.data))
                logging.info(f"Wrote {len(self.data)} lines to {self.filename}")
        except Exception as e:
            logging.error(f"Failed to write to file {self.filename}: {e}")
        finally:
            self.data = []


class ConsoleOutputHandler(OutputHandler):
    def __init__(self):
        self.data: List[str] = []
        logging.debug("ConsoleOutputHandler initialized")

    def save_to_buffer(self, data: str):
        self.data.append(data)
        logging.debug(f"Buffered data for console output: {data}")

    def write_output(self):
        try:
            for item in self.data:
                print(item)
        except Exception as e:
            logging.error(f"Failed to print to console: {e}")
        finally:
            self.data = []


class CSVOutputHandler(OutputHandler):
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.is_file_inited = False
        logging.debug(f"CSVOutputHandler initialized for file: {self.filename}")

    def save_to_buffer(self, data: Dict):
        self.data.append(data)
        logging.debug(f"Buffered data for CSV output: {data}")

    def write_output(self):
        if not self.data:
            logging.debug("No data to write for CSV output.")
            return
        try:
            with open(self.filename, mode="a", newline="") as file:
                fieldnames = self.data[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if not self.is_file_inited:
                    writer.writeheader()
                    self.is_file_inited = True
                    logging.debug("Wrote header to CSV file.")
                writer.writerows(self.data)
                logging.info(f"Wrote {len(self.data)} rows to {self.filename}")
        except Exception as e:
            logging.error(f"Failed to write to CSV file {self.filename}: {e}")
        finally:
            self.data = []
