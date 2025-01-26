from flask import Blueprint, render_template, request, session
import pandas as pd
import plotly.graph_objects as go
from ..db.db_operations import *

# Define the Blueprint
environmental_analysis_bp = Blueprint('environmental_analysis', __name__, template_folder='../../templates')

@environmental_analysis_bp.route('/', methods=['GET', 'POST'])
def environmental_analysis():
    conn, cursor = None, None

    # Fetch options for cancer type dropdown
    cancer_types = get_cancer_types()
    if cancer_types is None:
        cancer_types = [{'id': '-', 'name': 'Error fetching data'}]



    # Get user inputs
    cancer_type = request.args.get('cancer_type', "-")
    # Default to air quality index
    factor = request.args.get('factor', "air_quality_index")  

    # Fetch data for the selected cancer type and factor
    data = fetch_environmental_vs_incidence(cancer_type, factor)

    # check if the data was fetched successfully
    if data is None:
        scatter_plot = None
    else:
        # Process data
        df = pd.DataFrame(data, columns=['state', 'environmental_factor', 'cancer_incidence_rate'])

        # Generate scatter plot
        scatter_plot = go.Figure()
        scatter_plot.add_trace(
            go.Scatter(
                x=df['environmental_factor'],
                y=df['cancer_incidence_rate'],
                mode='markers',
                marker=dict(size=10, color='purple'),
                text=df['state'],
                name=f"{factor.replace('_', ' ').title()} vs Cancer Incidence"
            )
        )
        scatter_plot.update_layout(
            title=f"{factor.replace('_', ' ').title()} vs Cancer Incidence Rate by State",
            xaxis_title=factor.replace('_', ' ').title(),
            yaxis_title="Cancer Incidence Rate (per 1,000)",
            height=600,
            width=800,
        )
        scatter_plot = scatter_plot.to_html(full_html=False)

    # Store the data directly in the session for the download button
    session['environmental_data'] = data

    # Render template
    return render_template(
        'environmental_analysis.html',
        scatter_plot=scatter_plot,
        data=data,
        cancer_types=cancer_types,
        cancer_type=cancer_type,
        selected_factor=factor
    )
