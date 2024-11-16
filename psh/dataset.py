"""
This module contains the function to load the dataset from the NREL PSH database.
"""

import pandas as pd

import psh.computed_columns


def _load_data() -> pd.DataFrame:
    """
    Load the dataset from the NREL PSH database.
    :return: The dataset as a pandas DataFrame.
    :rtype: pandas.DataFrame
    """

    # Load the dataset
    nrel_psh = pd.read_csv("hf://datasets/ccm/nrel-psh/PSH_Export.csv")

    # Remove '$' and convert to numeric
    nrel_psh["System Cost (2022 US Dollars per Installed Kilowatt)"] = (
        nrel_psh["System Cost (2022 US Dollars per Installed Kilowatt)"]
        .str.replace("$", "", regex=False)
        .astype(float)
    )

    # Compute the L:H Ratio
    for function in psh.computed_columns.__all__:
        # Apply function to every row in dataset
        nrel_psh = nrel_psh.apply(getattr(psh.computed_columns, function), axis=1)

    return nrel_psh


DATA = _load_data()
