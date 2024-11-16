"""
This module provides a function to sort the dataset based on weighted sum of fields.
"""

from .dataset import DATA

import pandas

fields_to_exclude_from_sorting = [
    "Scenario System ID",
    "Upper Reservoir Geometry ID",
    "Lower Reservoir Geometry ID",
    "J40 Disadvantaged Community",
    "Coal Closure Community",
    "Fossil Fuel Employment Energy Community",
    "Existing Upper",
    "Existing Lower",
    "Longitude",
    "Latitude",
]


def sort_data(*weights_and_cutoffs: float) -> pandas.DataFrame:
    """Loads the dataset, applies cutoffs, calculates weighted sum, and sorts the data.

    Args:
        *weights_and_cutoffs: A sequence containing weights for each field
            followed by minimum and maximum cutoff values for each field.

    Returns:
        pandas.DataFrame: The sorted DataFrame.
    """

    # Copy the data for manipulation
    df = DATA.copy()

    # Determine sorting fields by excluding fields_to_exclude_from_sorting
    sorting_fields = [
        field for field in DATA.columns if field not in fields_to_exclude_from_sorting
    ]

    # Get number of fields
    n_fields = len(sorting_fields)

    # Extract weights and cutoffs
    weights = weights_and_cutoffs[:n_fields]
    min_cutoffs_values = weights_and_cutoffs[n_fields : 2 * n_fields]
    max_cutoffs_values = weights_and_cutoffs[2 * n_fields :]

    # Apply cutoffs
    for field, min_cutoff, max_cutoff in zip(
        sorting_fields, min_cutoffs_values, max_cutoffs_values
    ):
        df = df[(df[field] >= min_cutoff) & (df[field] <= max_cutoff)]

    # Calculate weighted sum
    weighted_sum = sum(
        [df[field] * weight for field, weight in zip(sorting_fields, weights)]
    )

    # Sort data by weighted sum
    sorted_df = df.assign(weighted_sum=weighted_sum).sort_values(
        by=["weighted_sum"], ascending=False
    )

    return sorted_df
