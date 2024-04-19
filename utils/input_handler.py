import abc
import logging
from typing import Any, Dict, Generator, List

import pandas as pd


class InputHandler(abc.ABC):
    @abc.abstractmethod
    def iter_input(self) -> Generator:
        pass

    @abc.abstractmethod
    def get_all_input(self) -> Any:
        pass


class FileInputHandler(InputHandler):
    def __init__(self, *, filename: str):
        self.filename = filename
        logging.debug(f"{type(self)} initialized with file: {self.filename}")

    def iter_input(self) -> Generator[str, None, None]:
        """
        Iteratively yield each line from a file, stripped of leading and trailing whitespace.
        """
        try:
            with open(self.filename, "r") as file:
                logging.debug("Opening file for line-by-line reading.")
                for line in file:
                    yield line.strip()
        except Exception as e:
            logging.error(f"Failed to read from file {self.filename}: {e}")
            raise

    def get_all_input(self) -> Any:
        try:
            with open(self.filename, "r") as file:
                logging.debug("Reading all content from file at once.")
                return file.read()
        except Exception as e:
            logging.error(f"Failed to read all content from file {self.filename}: {e}")
            raise


class ConsoleInputHandler(InputHandler):
    def __init__(self, *, welcome_msg: str = ""):
        self.welcome_msg = welcome_msg
        logging.debug("ConsoleInputHandler initialized with custom welcome message.")

    def iter_input(self) -> Generator[str, None, None]:
        logging.debug("Starting to read console input iteratively.")
        try:
            while data := input(self.welcome_msg):
                yield data
        except Exception as e:
            logging.error(f"Error reading input: {e}")
            raise

    def get_all_input(self) -> Any:
        logging.debug("Reading multiple console inputs until blank line.")
        data = []
        try:
            while row := input(self.welcome_msg):
                if not row:
                    break
                data.append(row)
            return data
        except Exception as e:
            logging.error(f"Error during reading multiple lines from console: {e}")
            raise


class CSVInputHandler(InputHandler):
    def __init__(self, filename: str):
        self.filename = filename
        logging.debug(f"PandasCSVInputHandler initialized with file: {self.filename}")

    def iter_input(self) -> Generator[Dict[Any, Any], None, None]:
        try:
            df = pd.read_csv(self.filename)
            logging.debug(
                "CSV file opened and read into DataFrame for iterative processing."
            )
            for _, row in df.iterrows():
                yield row.to_dict()
        except Exception as e:
            logging.error(
                f"Error processing CSV file iteratively: {self.filename}: {e}"
            )
            raise

    def get_all_input(self) -> List[Dict[Any, Any]]:
        try:
            df = pd.read_csv(self.filename)
            logging.debug("CSV file opened and converted to list of dictionaries.")
            return df.to_dict("records")
        except Exception as e:
            logging.error(
                f"Error reading CSV file into list of dictionaries: {self.filename}: {e}"
            )
            raise


def main():
    print(ConsoleInputHandler().get_all_input())
    print(FileInputHandler(filename="config.py").get_all_input())
    print(CSVInputHandler(filename="abcd.csv").get_all_input())


if __name__ == "__main__":
    main()
