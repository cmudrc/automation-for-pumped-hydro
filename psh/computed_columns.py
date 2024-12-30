"""
This module contains functions for computing additional columns for the given row of data. These functions are
automatically detected and used to transform data rows.

To write a valid function for this application, follow these guidelines:
1. The function must take a single argument of type `pandas.Series`.
2. The function must return a `pandas.Series`.
3. The function should add or modify columns in the input `pandas.Series`.

Example:
```python
def compute_example(row: pandas.Series) -> pandas.Series:
    row["Example Column"] = row["Some Column"] * 2
    return row
```
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


# def compute_remoteness(row: pandas.Series) -> pandas.Series:
#     """
#     Compute remoteness based on the distance to the nearest grocery store.
#     :param row: The row of data.
#     :type row: pandas.Series
#     :return: The row with additional columns.
#     :rtype: pandas.Series
#     """
#
#     # Pull lat and long from row
#     reservoir_lat = row["Latitude"]
#     reservoir_lon = row["Longitude"]
#
#     # Fetch nearby grocery stores (the threshold is defined in the function)
#     grocery_stores = fetch_grocery_stores(reservoir_lat, reservoir_lon)
#
#     # If no grocery stores are found, mark as remote
#     row["Remote (Computed)"] = grocery_stores.empty
#
#     print(row["Remote (Computed)"])
#
#     return row
#
#
# def compute_water_availability(row: pandas.Series) -> pandas.Series:
#     # Pull lat and long from row
#     # Look up location
#     # Measure distance to creek/river/lake?
#     # https://hub.arcgis.com/datasets/esri::usa-detailed-water-bodies/about
#     row["Water Availability"] = False
#     return row


# Only export the functions that transform rows
LOCALS = locals()
__all__ = [
    name
    for name in LOCALS  # iterate over everything in the current module
    if callable(LOCALS[name])  # has to be a function
    and len(LOCALS[name].__annotations__.values())
    == 2  # has to have one input and one output (1+1=2)
    and all(
        val == pandas.Series for val in LOCALS[name].__annotations__.values()
    )  # has to have all typehints of type Series
]
