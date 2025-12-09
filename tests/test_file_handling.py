"""
This file is used to test function in 'file_handling.py' file
"""

import os
import re
import pytest
from utils.file_handling import (
    get_transaction_file,
    read_csv_file,
    verify_csv_file,
    InvalidCSVFileError,
)


# #################################################
# #### get_transaction_file ########################
# #################################################


# Invalid folder path
def test_get_transaction_file_empty_folder(tmp_path):
    """
    Test function get_transaction_file for empty folder
    """
    folder_path = str(tmp_path)
    pattern = "invalid_pattern_1"
    accepted_extension = ".csv"
    with pytest.raises(
        FileNotFoundError,
        match=rf"No transaction file with pattern '{pattern}' and extension '{accepted_extension}' found in folder '{re.escape(folder_path)}'",
    ):
        get_transaction_file(folder_path=folder_path, pattern=pattern)


# Invalid pattern
def test_get_transaction_file_invalid_pattern(tmp_path):
    """
    Test function get_transaction_file for invalid pattern
    """
    folder_path = str(tmp_path)
    invalid_pattern = "invalid_pattern_1"
    extension = ".csv"
    # Create tmpfile for test
    tmp_file = tmp_path / f"proper_extension{extension}"
    tmp_file.write_text("proper exxtention")

    with pytest.raises(
        FileNotFoundError,
        match=rf"No transaction file with pattern '{invalid_pattern}' and extension '{extension}' found in folder '{re.escape(folder_path)}'",
    ):
        assert get_transaction_file(
            folder_path=folder_path, pattern=invalid_pattern, extension=extension
        )


# Invalid folder path
def test_get_transaction_file_invalid_folder():
    """
    Test function get_transaction_file for invalid folder path
    """
    invalid_folder_path = "dummy_mummy"
    invalid_pattern = "invalid_pattern_1"
    with pytest.raises(
        FileNotFoundError,
        match=f"There is no folder '{invalid_folder_path}'. Please verify.",
    ):
        get_transaction_file(folder_path=invalid_folder_path, pattern=invalid_pattern)


# Invalid extension
def test_get_transaction_file_invalid_extension(tmp_path):
    """
    Test function get_transaction_file for invalid extension
    """
    folder_path = str(tmp_path)
    pattern = "pattern_1_invalid_extension"
    accepted_extension = ".csv"

    # Create tmp file for test
    tmp_file = tmp_path / f"{pattern}.txt"
    tmp_file.write_text("invalid extention")

    with pytest.raises(
        FileNotFoundError,
        match=rf"No transaction file with pattern '{pattern}' and extension '{accepted_extension}' found in folder '{re.escape(folder_path)}'",
    ):
        assert get_transaction_file(folder_path=folder_path, pattern=pattern)


# happy path
def test_get_transaction_file_success(tmp_path):
    """
    Test function get_transaction_file for success scenario
    """
    folder_path = str(tmp_path)
    valid_pattern = "pattern_success"
    accepted_extension = ".csv"

    # Create tmp file
    tmp_file = tmp_path / f"{valid_pattern}{accepted_extension}"
    tmp_file.write_text("Success")

    output = get_transaction_file(
        folder_path=folder_path,
        pattern=valid_pattern,
        extension=accepted_extension,
    )

    assert output == os.path.join(folder_path, f"{valid_pattern}{accepted_extension}")


# #################################################
# #### read_csv_file ##############################
# #################################################


# success_all_data
def test_read_csv_file_success_all_data2(tmp_path):
    """
    Test read_csv_file function for success with all data at once
    """

    # Create file
    file_path = tmp_path / "all_data.csv"
    # file_path.write_text(
    #     "Data transakcji;Data ksi�gowania;Dane kontrahenta;Tytu�;Nr rachunku;Nazwa banku;Szczeg�y;Nr transakcji;Kwota transakcji (waluta rachunku);Waluta;Kwota blokady/zwolnienie blokady;Waluta;Kwota p�atno�ci w walucie;Waluta;Konto;Saldo po transakcji;Waluta\n27.11.2025;; ZEN.COM UAB  Vilnius LT09320 LTU ; P�atno�� kart�  27.11.2025 Nr karty 4246xx2886;;;;;;;-190;PLN;;;KONTO Direct - KD;2,04;PLN\n27.11.2025;27.11.2025; W�JCIK MATEUSZ TYSI�CLECIA 16/11 KATOWICE ; Przelew w�asny wyp�ata hcl;'70105012721000009131748106 ';ING Bank �l�ski S.A.;PRZELEW  ;'202533197201186845';14955;PLN;;;;;D�ugoterminowe wsp�lne;16729,7;PLN",
    #     encoding="utf-8",
    # )
    file_path = r"C:\Users\Wuyo2\Desktop\Wuyo\2_Code\m002_ing\files\Lista_transakcji_nr_0225963742_271125_prepared.csv"
    gen = read_csv_file(str(file_path), custom_separator=";", custom_chunksize=1000)
    output = next(gen)
    assert len(output) == 1000


# success_all_data
def test_read_csv_file_success_all_data(tmp_path):
    """
    Test read_csv_file function for success with all data at once
    """
    # Create file
    file_path = tmp_path / "all_data.csv"
    file_path.write_text("col1,col2\n1,2\n3,4\n5,6\n7,8\n9,10")

    gen = read_csv_file(str(file_path), custom_chunksize=1000)
    output = next(gen)
    assert len(output) == 5


# success_different_separator
def test_read_csv_file_success_different_separator(tmp_path):
    """
    Test read_csv_file function for success with all data at once
    """
    # Create file
    file_path = tmp_path / "all_data.csv"
    file_path.write_text("col1$col2\n1$2\n3$4\n5$6\n7$8\n9$10")

    gen = read_csv_file(str(file_path), custom_separator="$", custom_chunksize=1000)
    output = next(gen)
    assert len(output) == 5


# success
def test_read_csv_file_success_chunks(tmp_path):
    """
    Test read_csv_file function for success scenario
    """
    # Create file
    file_path = tmp_path / "all_data.csv"
    file_path.write_text("col1,col2\n1,2\n3,4\n5,6\n7,8\n9,10")

    custom_chunksize = 2

    gen = read_csv_file(file_path, custom_chunksize=custom_chunksize)
    output = next(gen)
    assert len(output) == custom_chunksize
    output = next(gen)
    assert len(output) == custom_chunksize
    output = next(gen)
    assert len(output) == 1


# #################################################
# #### verify_csv_file ##############################
# #################################################


# missing_file
def test_verify_csv_file_missing_file(tmp_path):
    """
    Test verify_csv_file function for missing file
    """

    file_path = tmp_path / "missing_file.csv"

    gen = read_csv_file(str(file_path))

    with pytest.raises(FileNotFoundError):
        verify_csv_file(gen, [])


# missing_columns
def test_verify_csv_file_missing_columns(tmp_path):
    """
    Test verify_csv_file function for missing columns
    """

    # Create file
    file_path = tmp_path / "all_data.csv"
    file_path.write_text("1,2\n3,4\n5,6\n7,8\n9,10")

    mandatory_cols = ["field_1", "field_2"]
    expected_error_message = (
        f"Provided CSV file missed the following headers: {', '.join(mandatory_cols)}"
    )
    gen = read_csv_file(str(file_path))

    with pytest.raises(InvalidCSVFileError, match=expected_error_message):
        verify_csv_file(gen, mandatory_cols)

    # Create file
    file_path = tmp_path / "all_data.csv"
    file_path.write_text("field_1,field_3\n1,2\n3,4\n5,6\n7,8\n9,10")

    mandatory_cols = ["field_1", "field_2"]
    expected_error_message = (
        f"Provided CSV file missed the following headers: {', '.join(["field_2"])}"
    )
    gen = read_csv_file(str(file_path))

    with pytest.raises(InvalidCSVFileError, match=expected_error_message):
        verify_csv_file(gen, mandatory_cols)


# missing_rows
def test_verify_csv_file_missing_rows(tmp_path):
    """
    Test verify_csv_file function for missing rows
    """

    # Create file
    file_path = tmp_path / "all_data.csv"
    file_path.write_text("field_1,field_2")

    mandatory_cols = ["field_1", "field_2"]
    expected_error_message = "Provided CSV file has no rows."
    gen = read_csv_file(str(file_path))

    with pytest.raises(InvalidCSVFileError, match=expected_error_message):
        verify_csv_file(gen, mandatory_cols)


# empty file
def test_verify_csv_file_empty_file(tmp_path):
    """
    Test verify_csv_file function for empty file
    """

    # Create file
    file_path = tmp_path / "all_data.csv"
    file_path.write_text("")

    mandatory_cols = ["field_1", "field_2"]
    expected_error_message = "Provided CSV file is empty. error message:"
    gen = read_csv_file(str(file_path))

    with pytest.raises(InvalidCSVFileError, match=expected_error_message):
        verify_csv_file(gen, mandatory_cols)


# success
def test_verify_csv_file_success(tmp_path):
    """
    Test verify_csv_file function for success.
    """

    # Create file
    file_path = tmp_path / "all_data.csv"
    file_path.write_text("field_1,field_3\n1,2\n3,4\n5,6\n7,8\n9,10")

    mandatory_cols = ["field_1", "field_3"]
    gen = read_csv_file(str(file_path))

    assert verify_csv_file(gen, mandatory_cols) is None
