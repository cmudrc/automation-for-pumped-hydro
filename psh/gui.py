"""
This module contains the Gradio interface for the PSH dataset.
"""

import gradio

from .dataset import DATA
from .ranking import sort_data, fields_to_exclude_from_sorting


# Define Gradio interface
def get_demo() -> gradio.Interface:
    """
    Create a Gradio interface for the PSH dataset.
    :return: The Gradio interface.
    :rtype: gradio.Interface
    """
    weights = []
    min_cutoffs = []  # List to store minimum cutoff sliders
    max_cutoffs = []  # List to store maximum cutoff sliders

    # Determine sorting fields by excluding fields_to_exclude_from_sorting
    sorting_fields = [
        field for field in DATA.columns if field not in fields_to_exclude_from_sorting
    ]

    with gradio.Blocks() as demo:
        for field in sorting_fields:
            with gradio.Row():
                # Get min/max values for the field
                min_val = DATA[field].min()
                max_val = DATA[field].max()

                # Create sliders for min and max cutoffs
                min_cutoff = gradio.Slider(
                    minimum=min_val,
                    maximum=max_val,
                    label=f"{field} Min Cutoff",
                    step=1,
                )
                min_cutoffs.append(min_cutoff)

                max_cutoff = gradio.Slider(
                    minimum=min_val,
                    maximum=max_val,
                    label=f"{field} Max Cutoff",
                    step=1,
                    value=max_val,
                )  # Set initial value to max
                max_cutoffs.append(max_cutoff)

                weight = gradio.Number(label=f"{field} Weight", value=1)
                weights.append(weight)

        output = gradio.DataFrame(label="Sorted Data")

        # Update change events
        for elem in min_cutoffs + max_cutoffs + weights:
            elem.change(
                sort_data, inputs=weights + min_cutoffs + max_cutoffs, outputs=output
            )

        demo.load(sort_data, inputs=weights + min_cutoffs + max_cutoffs, outputs=output)

    return demo
