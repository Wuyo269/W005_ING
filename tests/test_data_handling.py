"""
This file is used to test function in 'file_handling.py' file
"""

import logging
import pytest
import pandas as pd
import numpy as np
from utils.data_handling import (
    transform_data,
    categorise_field,
    categorise_contractor,
    categorise_title,
    start_with_no_category,
    no_category_dict,
)


# #################################################
# #### transform_data #############################
# #################################################


@pytest.fixture
def raw_data():
    data = pd.DataFrame(
        {
            "Amount": [
                "100,50",
                "-250,75",
                "45,25",
                "-120,00",
                "330,99",
                "-75,50",
                "200,00",
                "-89,25",
                "150,75",
                "",
                "",
            ],
            "Account": [
                "KONTO Direct - KD",
                "KONTO Direct - KD",
                "KONTO Direct - KD",
                "another accout",
                "another accout",
                "another accout",
                "KONTO Direct - KD",
                "KONTO Direct - KD",
                "KONTO Direct - KD",
                "KONTO Direct - KD",
                "KONTO Direct - KD",
            ],
        }
    )
    return data


@pytest.fixture
def raw_data_account():
    data = pd.DataFrame(
        {
            "Amount": [
                "-100,50",
                "-100,50",
                "-100,50",
                "-100,50",
                "-100,50",
                "-100,50",
            ],
            "Account": [
                "KONTO Direct - KD",
                "KONTO Direct - KD",
                "KONTO Direct - KD",
                "another accout",
                "another accout",
                "another accout",
            ],
        }
    )
    return data


@pytest.fixture
def amount_field_name():
    return "Amount"


@pytest.fixture
def account_field_name():
    return "Account"


@pytest.fixture
def mandatory_fields(
    amount_field_name, account_field_name
):  # pylint: disable=redefined-outer-name
    return [amount_field_name, account_field_name]


# Keep mandatory fields
@pytest.mark.transform_data
def test_transform_data_keep_only_mandatory_fields(
    raw_data, mandatory_fields, amount_field_name, account_field_name
):  # pylint: disable=redefined-outer-name

    raw_data["another_field"] = "No"
    raw_data["another_field_2"] = "yes"

    data = transform_data(
        raw_data,
        mandatory_fields,
        amount_field_name,
        account_field_name,
        "KONTO Direct - KD",
    )

    input_fields = raw_data.columns.tolist()
    mandatory_fields_extended = mandatory_fields.copy()
    mandatory_fields_extended.extend(["another_field", "another_field_2"])
    assert input_fields == mandatory_fields_extended
    output_fields = data.columns.tolist()
    assert output_fields == mandatory_fields


# missing mandatory fields
@pytest.mark.transform_data
def test_transform_data_missing_mandatory_field(
    raw_data, mandatory_fields, amount_field_name, account_field_name
):  # pylint: disable=redefined-outer-name

    mandatory_fields.append("mandaory_field_3")
    mandatory_fields.append("mandaory_field_4")

    with pytest.raises(KeyError):
        transform_data(
            raw_data,
            mandatory_fields,
            amount_field_name,
            account_field_name,
            "KONTO Direct - KD",
        )


# Remove na values
@pytest.mark.transform_data
def test_transform_data_remove_na(
    raw_data, mandatory_fields, amount_field_name, account_field_name
):  # pylint: disable=redefined-outer-name

    na_data = raw_data[raw_data["Amount"] == ""]
    assert len(na_data) > 0

    data = transform_data(
        raw_data,
        mandatory_fields,
        amount_field_name,
        account_field_name,
        "KONTO Direct - KD",
    )

    na_data = data[data["Amount"] == ""]
    assert len(na_data) == 0


# filter by account
@pytest.mark.transform_data
def test_transform_filter_by_account(
    raw_data_account, mandatory_fields, amount_field_name, account_field_name
):  # pylint: disable=redefined-outer-name

    assert len(raw_data_account) == 6

    data = transform_data(
        raw_data_account,
        mandatory_fields,
        amount_field_name,
        account_field_name,
        "KONTO Direct - KD",
    )

    assert len(data) == 3


# unify decimal points
@pytest.mark.transform_data
def test_transform_unify_decimal_points(
    mandatory_fields, amount_field_name, account_field_name
):  # pylint: disable=redefined-outer-name

    data = pd.DataFrame(
        {
            "Amount": [
                "-100,50",
                "-250,75",
                "-45,25",
            ],
            "Account": [
                "KONTO Direct - KD",
                "KONTO Direct - KD",
                "KONTO Direct - KD",
            ],
        }
    )
    assert data.iloc[0, 0] == "-100,50"
    assert data.iloc[1, 0] == "-250,75"
    assert data.iloc[2, 0] == "-45,25"

    data = transform_data(
        data,
        mandatory_fields,
        amount_field_name,
        account_field_name,
        "KONTO Direct - KD",
    )

    assert data.iloc[0, 0] == np.float64("-100.50")
    assert data.iloc[1, 0] == np.float64("-250.75")
    assert data.iloc[2, 0] == np.float64("-45.25")


# unify decimal points - int64
@pytest.mark.transform_data
def test_transform_unify_decimal_points_int64(
    mandatory_fields, amount_field_name, account_field_name
):  # pylint: disable=redefined-outer-name

    data = pd.DataFrame(
        {
            "Amount": [
                -100,
                -200,
                -300,
            ],
            "Account": [
                "KONTO Direct - KD",
                "KONTO Direct - KD",
                "KONTO Direct - KD",
            ],
        }
    )
    assert data.iloc[0, 0] == -100
    assert data.iloc[1, 0] == -200
    assert data.iloc[2, 0] == -300

    data = transform_data(
        data,
        mandatory_fields,
        amount_field_name,
        account_field_name,
        "KONTO Direct - KD",
    )

    assert data.iloc[0, 0] == np.int64("-100")
    assert data.iloc[1, 0] == np.int64("-200")
    assert data.iloc[2, 0] == np.int64("-300")


# keep_only_negative_numbers
@pytest.mark.transform_data
def test_transform_keep_only_negative_numbers(
    mandatory_fields, amount_field_name, account_field_name
):  # pylint: disable=redefined-outer-name

    data = pd.DataFrame(
        {
            "Amount": [
                "100,50",
                "250,75",
                "-45,25",
            ],
            "Account": [
                "KONTO Direct - KD",
                "KONTO Direct - KD",
                "KONTO Direct - KD",
            ],
        }
    )
    assert len(data) == 3

    data = transform_data(
        data,
        mandatory_fields,
        amount_field_name,
        account_field_name,
        "KONTO Direct - KD",
    )
    assert len(data) == 1


# #################################################
# #### categorise_field ###########################
# #################################################


@pytest.fixture
def field_data():
    data = pd.DataFrame(
        {
            "Dane kontrahenta": [
                "Lidl Polska",
                "Płatność Smart Gym ",
                "Kiosk",
                "Rybny",
                "Value5",
                "lidl Polska",
                "Kiosk",
                "Płatność Smart Gym ",
                "LIDL Polska",
            ]
        }
    )
    return data


@pytest.fixture
def field_mapping():
    mapping = {
        "APTEKA": "APTEKA",
        "Lidl": "LIDL",
        "Smart Gym": "FITNESS",
    }

    return mapping


# missing column
@pytest.mark.categorise_field
def test_categorise_field_missing_column(
    field_data, field_mapping
):  # pylint: disable=redefined-outer-name

    with pytest.raises(KeyError):
        assert categorise_field(field_data, field_mapping, "Contractor")


# missing column lowercase
@pytest.mark.categorise_field
def test_categorise_field_lowercase_column(
    caplog, field_data, field_mapping
):  # pylint: disable=redefined-outer-name

    caplog.set_level(logging.DEBUG)
    with pytest.raises(KeyError):
        assert categorise_field(field_data, field_mapping, "dane kontrahenta")
    assert "Available fields" in caplog.text


# no category column
@pytest.mark.categorise_field
def test_categorise_field_no_category_column(
    field_data, field_mapping
):  # pylint: disable=redefined-outer-name

    data = categorise_field(field_data, field_mapping, "Dane kontrahenta")
    input_fields = field_data.columns.tolist()
    assert "category" not in input_fields
    output_fields = data.columns.tolist()
    assert "category" in output_fields


# category column exist
@pytest.mark.categorise_field
def test_categorise_field_category_column_exists(
    field_data, field_mapping
):  # pylint: disable=redefined-outer-name

    field_data["category"] = "NO CATEGORY"
    data = categorise_field(field_data, field_mapping, "Dane kontrahenta")
    input_fields = field_data.columns.tolist()
    assert "category" in input_fields
    output_fields = data.columns.tolist()
    assert "category" in output_fields


@pytest.mark.categorise_field
def test_categorise_field_no_category_default(
    field_data, field_mapping
):  # pylint: disable=redefined-outer-name
    data = categorise_field(field_data, field_mapping, "Dane kontrahenta")
    # Kiosk, Rybny, Value5 should remain NO CATEGORY
    no_category_mask = ~data["category"].isin(["LIDL", "FITNESS"])
    assert data.loc[no_category_mask, "category"].eq("NO CATEGORY").all()


# happy path
@pytest.mark.categorise_field
def test_categorise_field_happy_path(
    field_data, field_mapping
):  # pylint: disable=redefined-outer-name

    data = categorise_field(field_data, field_mapping, "Dane kontrahenta")
    assert sum(data["category"] == "LIDL") == 3
    assert data.iloc[0, 1] == "LIDL"
    assert data.iloc[5, 1] == "LIDL"
    assert data.iloc[8, 1] == "LIDL"

    assert data.iloc[1, 1] == "FITNESS"
    assert data.iloc[7, 1] == "FITNESS"

    assert len(data) == len(field_data)


# #################################################
# #### categorise_contractor ######################
# #################################################


@pytest.fixture
def contractor_data():
    data = pd.DataFrame(
        {
            "Dane kontrahenta": [
                "Lidl Polska",
                "Płatność Smart Gym ",
                "Kiosk",
                "Rybny",
                "Value5",
                "lidl Polska",
                "Kiosk",
                "Płatność Smart Gym ",
                "LIDL Polska",
            ]
        }
    )
    return data


@pytest.fixture
def contractor_mapping():
    mapping = {
        "APTEKA": "APTEKA",
        "Lidl": "LIDL",
        "Smart Gym": "FITNESS",
    }

    return mapping


@pytest.mark.categorise_contractor
def test_categorise_contractor_no_category_default(
    contractor_data, contractor_mapping
):  # pylint: disable=redefined-outer-name
    data = categorise_contractor(contractor_data, contractor_mapping)
    # Kiosk, Rybny, Value5 should remain NO CATEGORY
    no_category_mask = ~data["category"].isin(["LIDL", "FITNESS"])
    assert data.loc[no_category_mask, "category"].eq("NO CATEGORY").all()


# happy path
@pytest.mark.categorise_contractor
def test_categorise_contractor_happy_path(
    contractor_data, contractor_mapping
):  # pylint: disable=redefined-outer-name

    data = categorise_contractor(
        contractor_data, contractor_mapping, "Dane kontrahenta"
    )
    assert sum(data["category"] == "LIDL") == 3
    assert data.iloc[0, 1] == "LIDL"
    assert data.iloc[5, 1] == "LIDL"
    assert data.iloc[8, 1] == "LIDL"

    assert data.iloc[1, 1] == "FITNESS"
    assert data.iloc[7, 1] == "FITNESS"

    assert len(data) == len(contractor_data)


# #################################################
# #### categorise_title ###########################
# #################################################


@pytest.fixture
def title_data():
    data = pd.DataFrame(
        {
            "Title": [
                "www.mediaexpert.pl",
                "Polaczki.male",
                "Wypłata gotówki",
                "Płatność za bilety.polregio.pl 20zł",
                "Value5",
                "lidl Polska",
                "Blik",
                "Płatność Smart Gym ",
                "Blik",
            ]
        }
    )
    return data


@pytest.fixture
def title_mapping():
    mapping = {
        "www.mediaexpert.pl": "MIESZKANIE",
        "bilety.polregio.pl": "TRANSPORT",
        "Wypłata gotówki": "GOTÓWKA",
        "Blik": "GOTÓWKA",
    }

    return mapping


@pytest.mark.categorise_title
def test_categorise_title_no_category_default(
    title_data, title_mapping
):  # pylint: disable=redefined-outer-name
    data = categorise_title(title_data, title_mapping, "Title")
    # Kiosk, Rybny, Value5 should remain NO CATEGORY
    no_category_mask = ~data["category"].isin(["MIESZKANIE", "TRANSPORT", "GOTÓWKA"])
    assert data.loc[no_category_mask, "category"].eq("NO CATEGORY").all()


# happy path
@pytest.mark.categorise_title
def test_categorise_title_happy_path(
    title_data, title_mapping
):  # pylint: disable=redefined-outer-name

    data = categorise_title(title_data, title_mapping, "Title")
    assert sum(data["category"] == "GOTÓWKA") == 3
    assert data.iloc[2, 1] == "GOTÓWKA"
    assert data.iloc[6, 1] == "GOTÓWKA"
    assert data.iloc[8, 1] == "GOTÓWKA"

    assert data.iloc[3, 1] == "TRANSPORT"
    # assert data.iloc[7, 1] == "FITNESS"

    assert len(data) == len(title_data)


# #################################################
# #### categorise_title ###########################
# #################################################

# No 'no category' rows
# 'No category' on top


@pytest.fixture
def no_category_data():
    data = pd.DataFrame(
        {
            "category": [
                "LIDL",
                "PIECZYWA",
                "BIEDRONKA",
                "NO CATEGORY",
                "NO CATEGORY",
                "PIECZYWA",
                "TRANSPORT",
                "NO CATEGORY",
                "NO CATEGORY",
                "BIEDRONKA",
                "NO CATEGORY",
                "NO CATEGORY",
            ]
        }
    )
    return data


# No 'no category' rows
def test_start_with_no_category_zero_no_category_rows(
    no_category_data,
):  # pylint: disable=redefined-outer-name

    no_category_data = no_category_data[no_category_data["category"] != "NO CATEGORY"]

    sorted_data = start_with_no_category(no_category_data)

    assert no_category_data.iloc[0, 0] == sorted_data.iloc[0, 0]
    assert no_category_data.iloc[1, 0] == sorted_data.iloc[1, 0]
    assert no_category_data.iloc[2, 0] == sorted_data.iloc[2, 0]


# 'No category' on top
def test_start_with_no_category_happy_path(
    no_category_data,
):  # pylint: disable=redefined-outer-name

    assert no_category_data.iloc[0, 0] != "NO CATEGORY"
    assert no_category_data.iloc[1, 0] != "NO CATEGORY"
    assert no_category_data.iloc[2, 0] != "NO CATEGORY"
    no_category_data = start_with_no_category(
        no_category_data, "category", "NO CATEGORY"
    )

    assert no_category_data.iloc[0, 0] == "NO CATEGORY"
    assert no_category_data.iloc[1, 0] == "NO CATEGORY"
    assert no_category_data.iloc[2, 0] == "NO CATEGORY"


# #################################################
# #### no_category_dict ###########################
# #################################################


@pytest.fixture
def no_category_dict_data():
    data = pd.DataFrame(
        {
            "title": [
                "majonez",
                "bulka",
                "krupnik",
                "Płatnośc telefonem",
                "Zgrzyt zębów 2. Odrodzenie",
            ],
            "category": [
                "LIDL",
                "PIECZYWA",
                "BIEDRONKA",
                "NO CATEGORY",
                "NO CATEGORY",
            ],
        }
    )
    return data


# data incorrect type
@pytest.mark.no_category_dict
def test_no_category_dict_data_incorrect_type():
    """
    Test if function raise TypeError if incorrect type will be provided
    """
    with pytest.raises(TypeError, match="Argument 'data' must be type pd.DataFrame"):
        _ = no_category_dict([])
    with pytest.raises(TypeError, match="Argument 'data' must be type pd.DataFrame"):
        _ = no_category_dict("not a dataframe")


# missing column
@pytest.mark.no_category_dict
def test_no_category_dict_missing_column(
    no_category_dict_data,
):  # pylint: disable=redefined-outer-name
    """
    Test if function raise KeyError if column is missing
    """
    with pytest.raises(KeyError):
        _ = no_category_dict(no_category_dict_data, "Sprzedawca", "kategorie", "Brak")


# Column exist but in lower case.
@pytest.mark.no_category_dict
def test_no_category_dict_lowercase_column(
    no_category_dict_data,
):  # pylint: disable=redefined-outer-name
    """
    Test if function raise KeyError if column is lowercase
    """
    with pytest.raises(KeyError):
        _ = no_category_dict(no_category_dict_data, "TITLE", "kategorie", "Brak")


# unfiltered data provided
@pytest.mark.no_category_dict
def test_no_category_dict_unfiltered_data(
    no_category_dict_data,
):  # pylint: disable=redefined-outer-name
    """
    Test if function return dictionary only for "no catego" data
    """

    unique = no_category_dict(no_category_dict_data, "title", "category", "NO CATEGORY")
    assert len(unique) == 2
    assert isinstance(unique, dict)
    assert "Płatnośc telefonem" in unique
    assert "Zgrzyt zębów 2. Odrodzenie" in unique


# # no data after filter
@pytest.mark.no_category_dict
def test_no_category_dict_return_no_data(
    no_category_dict_data,
):  # pylint: disable=redefined-outer-name
    """
    Test if function return empty dictionary
    """
    no_category_dict_data = no_category_dict_data[
        no_category_dict_data["category"] != "NO CATEGORY"
    ]
    unique = no_category_dict(no_category_dict_data, "title", "category", "NO CATEGORY")
    assert len(unique) == 0
    assert unique == {}


# happy path
@pytest.mark.no_category_dict
def test_no_category_dict_only_no_category(
    no_category_dict_data,
):  # pylint: disable=redefined-outer-name
    """
    Test if function return empty dictionary
    """
    no_category_dict_data = no_category_dict_data[
        no_category_dict_data["category"] == "NO CATEGORY"
    ]
    unique = no_category_dict(no_category_dict_data, "title", "category", "NO CATEGORY")
    assert len(unique) == 2
    assert isinstance(unique, dict)
    assert "Płatnośc telefonem" in unique
    assert "Zgrzyt zębów 2. Odrodzenie" in unique
