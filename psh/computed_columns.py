"""
This module contains functions for computing additional columns for the given row of data.
"""

import pandas as __pandas


def dummy_demo(row: __pandas.Series) -> __pandas.Series:
    """
    Take the row, and just return it as is.
    :param row: The row.
    :type row: pandas.Series
    :return: The row.
    :rtype: pandas.Series
    """

    return row


def compute_lh_ratio(row: __pandas.Series) -> __pandas.Series:
    """
    Compute additional columns for the given row of data.
    :param row: The row of data.
    :type row: pandas.Series
    :return: The row with additional columns.
    :rtype: pandas.Series
    """
    # Compute the L:H Ratio
    row["L:H Ratio (Computed)"] = (
        row["Horizontal Distance Between Reservoirs (Meters)"]
        / row["System Average Hydraulic Head (Meters)"]
    )

    return row


def compute_remoteness(row: __pandas.Series) -> __pandas.Series:
    # Pull lat and long from row
    # Look up location
    # Measure distance to civilization?
    row["Remote"] = False
    return row

def compute_water_availability(row: __pandas.Series) -> __pandas.Series:
    # Pull lat and long from row
    # Look up location
    # Measure distance to creek/river/lake?
    # https://hub.arcgis.com/datasets/esri::usa-detailed-water-bodies/about
    row["Water Availability"] = False
    return row

# Define __all__ dynamically
__all__ = [name for name in locals() if not name.startswith("__")]
