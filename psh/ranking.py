from .dataset import load_data

# Load the dataset
nrel_psh = load_data()

# Define all fields
sorting_fields = [
    # "Scenario System ID",
    # "Upper Reservoir Geometry ID",
    # "Lower Reservoir Geometry ID",
    "Upper Reservoir Dam Height (Meters)",
    "Lower Reservoir Dam Height (Meters)",
    "Horizontal Distance Between Reservoirs (Meters)",
    "System Average Hydraulic Head (Meters)",
    "L:H Ratio (Water Conveyance Length to Head Height Ratio)",
    "Upper Reservoir Water Volume (Gigaliters)",
    "Lower Reservoir Water Volume (Gigaliters)",
    "Upper Dam Rock Volume (Gigaliters)",
    "Lower Dam Rock Volume (Gigaliters)",
    "System Water Requirement (Gigaliters)",
    "Effective System Water Volume (Gigaliters)",
    "System Reservoir Volume Percent Difference",
    "System Energy Storage Capacity (Gigawatt hours)",
    "System Installed Capacity (Megawatts)",
    "System Cost (2022 US Dollars per Installed Kilowatt)",
    # "J40 Disadvantaged Community",
    # "Coal Closure Community",
    # "Fossil Fuel Employment Energy Community",
    # "Existing Upper",
    # "Existing Lower",
    # "Longitude", "Latitude"
]


def sort_data(*weights_and_cutoffs):
    """Loads the dataset, applies cutoffs, calculates weighted sum, and sorts the data.

    Args:
        *weights_and_cutoffs: A sequence containing weights for each field
            followed by minimum and maximum cutoff values for each field.

    Returns:
        pandas.DataFrame: The sorted DataFrame.
    """

    n_fields = len(sorting_fields)

    weights = weights_and_cutoffs[:n_fields]
    min_cutoffs_values = weights_and_cutoffs[n_fields : 2 * n_fields]
    max_cutoffs_values = weights_and_cutoffs[2 * n_fields :]

    df = nrel_psh.copy()

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
