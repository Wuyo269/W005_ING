"""
This file contains all method related to files:
-get_transaction_file
-read_csv_file
-verify_csv_file
"""

import logging
import os
import pandas as pd

LOGGER = logging.getLogger(__name__)


def get_transaction_file(
    folder_path: str, pattern: str = "lista_transakcji_nr_", extension: str = ".csv"
) -> str:
    """
    Get path to transaction file from provided folder with data
    """
    LOGGER.debug("Input argument - folder_path: %s", folder_path)
    LOGGER.debug("Input argument - pattern: %s", pattern)

    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"There is no folder '{folder_path}'. Please verify."
        ) from None
    LOGGER.debug("Number of files in folder: %s", len(files))

    for file in files:
        if (
            os.path.basename(file).lower().startswith(pattern.lower())
            and os.path.splitext(file)[-1].lower() == extension.lower()
        ):
            file_path = os.path.join(folder_path, file)
            LOGGER.debug("Selected file: %s", file_path)
            return file_path

    raise FileNotFoundError(
        f"No transaction file with pattern '{pattern}' and extension '{extension}' found in folder '{folder_path}'",
    )


def read_csv_file(file_path: str, custom_separator=",", custom_chunksize=100):
    """
    Read data from CSV file in chunks
    Rerurn generator of dataframes
    """
    # Encoding: latin1
    # Encoding: cp1250
    yield from pd.read_csv(
        file_path, sep=custom_separator, encoding="cp1250", chunksize=custom_chunksize
    )


class InvalidCSVFileError(Exception):
    """Custom exception for invalid CSV files."""


def verify_csv_file(gen, mandatory_columns: list[str]):
    """
    Verify if CSV file is valid.
    Check for:
    -missing rows
    -missing columns
    -empty file"""

    try:
        data = next(gen)
        if data.empty:
            raise InvalidCSVFileError("Provided CSV file has no rows.")
        columns = data.columns.tolist()
        missing_mandatory_columns = [c for c in mandatory_columns if c not in columns]
        if any(missing_mandatory_columns):
            raise InvalidCSVFileError(
                f"Provided CSV file missed the following headers: {', '.join(missing_mandatory_columns)}"
            )
    except pd.errors.EmptyDataError as e:
        raise InvalidCSVFileError(
            f"Provided CSV file is empty. error message: '{e}'"
        ) from None
