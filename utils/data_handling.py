"""
This file contains all method related to data transformation:
    -transform data
    -categorise_field
    -categorise_contractor
    -categorise_title

"""

import logging
import pandas as pd
import numpy as np


LOGGER = logging.getLogger(__name__)


def transform_data(
    data_chunk: pd.DataFrame,
    mandatory_fields: list[str],
    amount_field_name: str = "Kwota transakcji (waluta rachunku)",
    account_field_name: str = "Konto",
    account_field_value: str = "KONTO Direct - KD",
) -> pd.DataFrame:
    """
    Transform chunk data base d on the following details:
    -Remove blocked transactions (transactions without amount)
    -Keep only data from account KONTO Direct - KD
    -Unify decimal point to "."
    -Keep only negative transactions (spendings)
    """

    fields = data_chunk.columns.tolist()
    missing_fields = [f for f in mandatory_fields if f not in fields]
    if missing_fields:
        raise KeyError(f"Missing mandatory fields: {', '.join(missing_fields)}")

    data = data_chunk[mandatory_fields].copy()
    # Convert empty string and whitespace into np.nan
    data[amount_field_name] = data[amount_field_name].replace(
        r"^\s*$", np.nan, regex=True
    )
    # Remove blocked transactions (transactions without amount)
    data = data.dropna(subset=[amount_field_name])
    data = data[data[account_field_name] == account_field_value]
    # In polish files "," character is set as decimal point.
    # Change it into "."
    col = data[amount_field_name].astype(str).str.replace(",", ".")
    data[amount_field_name] = col.astype(float)

    data = data[data[amount_field_name] < 0]
    return data


def categorise_field(
    data: pd.DataFrame, categories: dict[str, str], field_name: str
) -> pd.DataFrame:
    """
    Categorise data in column 'field_name' based on provided mapping 'categories'.
    """

    fields = data.columns.tolist()
    if field_name not in fields:
        LOGGER.debug(
            "Field '%s' does not exist. Available fields: %s",
            field_name,
            fields,
        )
        raise KeyError(f"Field '{field_name}' does not exist.")

    data = data.copy()
    if "category" not in fields:
        data["category"] = "NO CATEGORY"

    lower_field = f"{field_name} lower"
    data[lower_field] = data[field_name].astype(str).str.lower()

    for key, category in categories.items():
        LOGGER.debug("Searching key: %s", key.lower())
        mask = data[lower_field].str.contains(key.lower(), na=False)
        LOGGER.debug("Found %d matches for key: %s", sum(mask), key.lower())
        data.loc[mask, "category"] = category

    return data.drop(lower_field, axis=1)


def categorise_contractor(
    data: pd.DataFrame,
    categories: dict[str, str],
    contractor_field_name: str = "Dane kontrahenta",
) -> pd.DataFrame:
    """
    Categorise data in column 'contractor_field_name' based on provided mapping 'categories'.
    """

    data = categorise_field(data, categories, contractor_field_name)
    return data


def categorise_title(
    data: pd.DataFrame,
    categories: dict[str, str],
    title_field_name: str = "Tytuł",
) -> pd.DataFrame:
    """
    Categorise data in column 'title_field_name' based on provided mapping 'categories'.
    """

    data = categorise_field(data, categories, title_field_name)
    return data


def start_with_no_category(
    data: pd.DataFrame,
    category_field: str = "category",
    no_category_value="NO CATEGORY",
) -> pd.DataFrame:
    """
    Sort data to place 'NO CATEGORY' items on top.
    """

    data = data.copy()
    return data.sort_values(by=category_field, key=lambda s: s != no_category_value)


def no_category_dict(
    data: pd.DataFrame,
    field: str = "title",
    category_field: str = "category",
    field_value: str = "NO CATEGORY",
) -> dict[str, str]:
    """
    Crete dictionary of unique values for specified category in provided field.
    By default funcion should create a dictionary of "NO CATEGORY" items in"category" field.

    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Argument 'data' must be type pd.DataFrame")
    data = data.copy()

    for f in [field, category_field]:
        if not f in data.columns:
            raise KeyError(f"Field '{f}' not found in DataFrame columns.")

    data = data[data[category_field] == field_value]
    unique_values = sorted(list(data[field].unique()))
    return {f: field_value for f in unique_values}
