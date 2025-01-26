from flask import Blueprint, render_template, request, session
from ..db.db_connector import get_db_connection
from ..db.insights_queries import *
from ..db.queries import *
import pandas as pd
import plotly.graph_objects as go

# Define the Blueprint
risk_factors_analysis_bp = Blueprint('risk_factors_analysis', __name__, template_folder='../../templates')

@risk_factors_analysis_bp.route('/', methods=['GET', 'POST'])
def risk_factors_analysis():
    conn, cursor = None, None

    # Fetch options for cancer type dropdown
    cancer_types = []
    try:
        conn, cursor = get_db_connection()
        cancer_types = [{'id': '-', 'name': 'All Cancer Types'}]
        cursor.execute(fetch_cancer_types_query())
        cancer_types += cursor.fetchall()
    except Exception as e:
        print(f"Error fetching dropdown options: {e}")
        cancer_types = [{'id': '-', 'name': 'Error fetching data'}]
    finally:
        if cursor:  
            cursor.close()
        if conn: 
            conn.close()


    # Get user inputs from the query string where - is the default value
    cancer_type = request.args.get('cancer_type', "-")
    # Default to cigarette use rate
    factor = request.args.get('factor', "cigarette_use_rate")  

    # Fetch data for the selected cancer type and factor
    data = []
    try:
        conn, cursor = get_db_connection()
        query = risk_factors_vs_incidence(cancer_type, factor)
        cursor.execute(query)
        data = cursor.fetchall()
    except Exception as e:
        print(f"Database query failed: {e}")
        data = None
    finally:
        if cursor:  
            cursor.close()
        if conn: 
            conn.close()

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