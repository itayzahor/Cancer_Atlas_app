from flask import Blueprint, render_template, request, session
import pandas as pd
import plotly.graph_objects as go
from ..db.db_operations import *

# Define the Blueprint
socioeconomic_analysis_bp = Blueprint('socioeconomic_analysis', __name__, template_folder='../../templates')

@socioeconomic_analysis_bp.route('/', methods=['GET', 'POST'])
def socioeconomic_analysis():
    # Fetch options for cancer type dropdown
    cancer_types = get_cancer_types()
    if cancer_types is None:
        cancer_types = [{'id': '-', 'name': 'Error fetching data'}]

    # Get user inputs from the query string where - is the default value
    cancer_type = request.args.get('cancer_type', "-")
    # Default to median_income
    factor = request.args.get('factor', "median_income") 

   # Fetch data for the selected cancer type and socioeconomic factor
    data = fetch_socioeconomic_vs_mortality(cancer_type, factor)
    
    # check if the data was fetched successfully
    if data is None:
        scatter_plot = None
    else:
        # Process and visualize data
        df = pd.DataFrame(data, columns=['state', 'socioeconomic_factor', 'mortality_rate'])
        scatter_plot = go.Figure()
        scatter_plot.add_trace(
            go.Scatter(
                x=df['socioeconomic_factor'],
                y=df['mortality_rate'],
                mode='markers',
                marker=dict(size=10, color='blue'),
                text=df['state'],
                name=f"{factor.replace('_', ' ').title()} vs Mortality"
            )
        )
        scatter_plot.update_layout(
            title=f"{factor.replace('_', ' ').title()} vs Cancer Mortality Rate by State",
            xaxis_title=factor.replace('_', ' ').title(),
            yaxis_title="Mortality Rate",
            height=600,
            width=800,
        )
        scatter_plot = scatter_plot.to_html(full_html=False)

    # Store the data directly in the session for the download button
    session['socioeconomic_data'] = data

    # Render the Insights page with the chart and data
    return render_template(
        'socioeconomic_analysis.html',
        scatter_plot=scatter_plot,
        data=data,
        cancer_types=cancer_types,
        cancer_type=cancer_type,
        factor=factor
    )
