from flask import Blueprint, render_template, request, session
import pandas as pd
import plotly.graph_objects as go
from ..db.db_operations import *

# Define the Blueprint
risk_factors_analysis_bp = Blueprint('risk_factors_analysis', __name__, template_folder='../../templates')

@risk_factors_analysis_bp.route('/', methods=['GET', 'POST'])
def risk_factors_analysis():
    # Fetch options for cancer type dropdown
    cancer_types = get_cancer_types()
    if cancer_types is None:
        cancer_types = [{'id': '-', 'name': 'Error fetching data'}]


    # Get user inputs from the query string where - is the default value
    cancer_type = request.args.get('cancer_type', "-")
    # Default to cigarette use rate
    factor = request.args.get('factor', "cigarette_use_rate")  

    # Fetch data for the selected cancer type and risk factor
    data = fetch_risk_factors_vs_incidence(cancer_type, factor)

    # check if the data was fetched successfully
    if data is None:
        scatter_plot = None
    else:
        # Process data
        df = pd.DataFrame(data, columns=['state', 'risk_factor', 'cancer_incidence_rate'])

        # Generate scatter plot
        scatter_plot = go.Figure()
        scatter_plot.add_trace(
            go.Scatter(
                x=df['risk_factor'],
                y=df['cancer_incidence_rate'],
                mode='markers',
                marker=dict(size=10, color='orange'),
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
    session['risk_factors_data'] = data 

    # Render template
    return render_template(
        'risk_factors_analysis.html',
        scatter_plot=scatter_plot,
        data=data,
        cancer_types=cancer_types,
        cancer_type=cancer_type,
        selected_factor=factor
    )