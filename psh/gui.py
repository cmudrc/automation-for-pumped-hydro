"""
This module contains the enhanced Gradio interface with Leaflet map visualization.
"""

import json

import gradio
import pandas as pd

from .dataset import DATA
from .ranking import sort_data, fields_to_exclude_from_sorting


def create_map_html(filtered_data: pd.DataFrame) -> str:
    """Create the map HTML with Leaflet."""
    # Convert valid points to GeoJSON for efficient processing
    valid_data = filtered_data.dropna(subset=["Latitude", "Longitude"])

    # Create feature collection
    features = []
    for _, row in valid_data.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(row["Longitude"]), float(row["Latitude"])],
            },
            "properties": {
                "scenario_id": str(row["Scenario System ID"]),
                "latitude": str(row["Latitude"]),
                "longitude": str(row["Longitude"]),
            },
        }
        features.append(feature)

    geojson_data = json.dumps({"type": "FeatureCollection", "features": features})

    # Create complete HTML document
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css"/>
        <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css"/>
        <style>
            html, body, #map {{
                height: 100%;
                width: 100%;
                margin: 0;
                padding: 0;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>
        <script>
            // Initialize map
            var map = L.map('map').setView([39.8283, -98.5795], 4);
            
            // Define base layers
            var osm = L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19,
                attribution: '© OpenStreetMap contributors'
            }});
            
            // ESRI World Imagery layer (free satellite imagery)
            var satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
                maxZoom: 19,
                attribution: 'Tiles © Esri — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
            }});
            
            // Set default layer
            osm.addTo(map);
            
            // Create base layers object for layer control
            var baseLayers = {{
                "OpenStreetMap": osm,
                "Satellite": satellite
            }};
            
            // Create marker cluster group
            var markers = L.markerClusterGroup();
            
            // Add GeoJSON data
            var geojsonData = {geojson_data};
            
            L.geoJSON(geojsonData, {{
                pointToLayer: function(feature, latlng) {{
                    return L.marker(latlng);
                }},
                onEachFeature: function(feature, layer) {{
                    var props = feature.properties;
                    layer.bindPopup(
                        "<b>Scenario ID:</b> " + props.scenario_id + "<br>" +
                        "<b>Latitude:</b> " + props.latitude + "<br>" +
                        "<b>Longitude:</b> " + props.longitude
                    );
                }}
            }}).addTo(markers);
            
            // Add markers to map
            map.addLayer(markers);
            
            // Add layer control
            L.control.layers(baseLayers, null, {{
                position: 'topright',
                collapsed: false
            }}).addTo(map);

            // Ensure map displays correctly in iframe
            setTimeout(function() {{ map.invalidateSize(); }}, 100);
        </script>
    </body>
    </html>
    """

    return f"""
    <div style="height:600px;width:100%;border:none;">
        <iframe 
            srcdoc="{html_content.replace('"', '&quot;')}"
            style="width:100%;height:100%;border:none;"
            sandbox="allow-scripts allow-same-origin">
        </iframe>
    </div>
    """


def get_demo() -> gradio.Blocks:
    """
    Create an enhanced Gradio interface with map visualization.
    """
    # Pre-calculate sorting fields
    sorting_fields = [
        field for field in DATA.columns if field not in fields_to_exclude_from_sorting
    ]

    # Pre-calculate min/max values
    field_ranges = {
        field: (DATA[field].min(), DATA[field].max()) for field in sorting_fields
    }

    weights = []
    min_cutoffs = []
    max_cutoffs = []

    with gradio.Blocks() as demo:
        with gradio.Row():
            # Left column for controls
            with gradio.Column(scale=1.5):
                for field in sorting_fields:
                    with gradio.Row():
                        min_val, max_val = field_ranges[field]

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
                        )
                        max_cutoffs.append(max_cutoff)

                        weight = gradio.Number(label=f"{field} Weight", value=1)
                        weights.append(weight)

            # Right column for visualization
            with gradio.Column(scale=1.5):
                # Reduced height of map container
                map_html = gradio.HTML(label="Location Map")
                # Slightly reduced height for table
                data_table = gradio.DataFrame(label="Sorted Data")

        def update_visualization(*args):
            filtered_data = sort_data(*args)
            map_html_content = create_map_html(filtered_data)
            return map_html_content, filtered_data

        # Update both visualizations on any input change
        update_inputs = weights + min_cutoffs + max_cutoffs
        update_outputs = [map_html, data_table]

        for elem in update_inputs:
            elem.change(
                update_visualization, inputs=update_inputs, outputs=update_outputs
            )

        # Initial load
        demo.load(update_visualization, inputs=update_inputs, outputs=update_outputs)

    return demo
