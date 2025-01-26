from flask import Blueprint, render_template, request, session
from ..db.db_connector import get_db_connection
from ..db.insights_queries import *
from ..db.queries import *
import pandas as pd
import plotly.graph_objects as go

# Define the Blueprint
socioeconomic_analysis_bp = Blueprint('socioeconomic_analysis', __name__, template_folder='../../templates')

@socioeconomic_analysis_bp.route('/', methods=['GET', 'POST'])
def socioeconomic_analysis():
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
    # Default to median_income
    factor = request.args.get('factor', "median_income") 

   # Fetch data for the selected cancer type and factor
    data = []
    try:
        conn, cursor = get_db_connection()
        query = socioeconomic_vs_mortality(cancer_type, factor)
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
