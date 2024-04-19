import logging

import typer

from config import setup_logging
from utils.input_handler import FileInputHandler
from utils.output_handler import FileOutputHandler

setup_logging()
logger = logging.getLogger(__name__)


def main(input_file: str, output_file: str):
    file_handler = FileInputHandler(filename=input_file)
    output_handler = FileOutputHandler(filename=output_file)
    for line in file_handler.iter_input():
        output_handler.save_to_buffer(line)
    output_handler.write_output()


if __name__ == "__main__":
    setup_logging()
    typer.run(main)
