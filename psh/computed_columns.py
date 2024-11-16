"""
This module contains functions for computing additional columns for the given row of data.
"""

import pandas


def compute_lh_ratio(row: pandas.Series) -> pandas.Series:
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


# Define __all__ dynamically
__all__ = [name for name in locals() if not name.startswith("__")]
