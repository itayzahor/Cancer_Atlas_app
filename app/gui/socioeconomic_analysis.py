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

    # Get database connection and cursor
    conn, cursor = get_db_connection()
    cancer_types = fetch_sites(cursor)
    cursor.close()
    conn.close()

    # Get user inputs
    cancer_type = request.args.get('cancer_type', "-")
    factor = request.args.get('factor', "median_income")  # Default to median_income

   # Fetch data based on user inputs
    conn, cursor = get_db_connection()
    try:
        query = socioeconomic_vs_mortality(cancer_type, factor)
        cursor.execute(query)
        data = cursor.fetchall()
    except Exception as e:
        print(f"Database query failed: {e}")
        data = []  # Fallback to empty data
    finally:
        cursor.close()
        conn.close()
    
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

    # Store the data directly in the session
    session['socioeconomic_data'] = data

    # Render the Insights page with the chart and data
    return render_template(
        'socioeconomic_analysis.html',
        scatter_plot=scatter_plot.to_html(full_html=False),
        data=data,
        cancer_types=cancer_types,
        cancer_type=cancer_type,
        factor=factor
    )
