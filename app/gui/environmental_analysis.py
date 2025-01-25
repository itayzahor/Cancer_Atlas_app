from flask import Blueprint, render_template, request, session
from ..db.db_connector import get_db_connection
from ..db.queries import *  
from ..db.insights_queries import *
import pandas as pd
import plotly.graph_objects as go

# Define the Blueprint
environmental_analysis_bp = Blueprint('environmental_analysis', __name__, template_folder='../../templates')

@environmental_analysis_bp.route('/', methods=['GET', 'POST'])
def environmental_analysis():
    # Fetch options for cancer type dropdown
    cancer_types = []
    try:
        conn, cursor = get_db_connection()
        cursor.execute(fetch_cancer_types_query())
        cancer_types = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching cancer types: {e}")
        # Log the error and potentially return a default value or error flag
        cancer_types = [{'id': '-', 'name': 'Error fetching data'}]
    finally:
        cursor.close()
        conn.close()


    # Get user inputs
    cancer_type = request.args.get('cancer_type', "-")
    factor = request.args.get('factor', "air_quality_index")  # Default to air quality index

    # Fetch data for the selected cancer type and factor
    data = []
    try:
        conn, cursor = get_db_connection()
        query = environmental_vs_incidence(cancer_type, factor)
        cursor.execute(query)
        data = cursor.fetchall()
    except Exception as e:
        print(f"Database query failed: {e}")
        # Return a flag or meaningful error message
        data = [{'error': f"Failed to fetch data for {factor}. Please try again later."}]
    finally:
        cursor.close()
        conn.close()

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

    # Store the data directly in the session
    session['environmental_data'] = data

    # Render template
    return render_template(
        'environmental_analysis.html',
        plot_html=scatter_plot.to_html(full_html=False),
        data=data,
        cancer_types=cancer_types,
        cancer_type=cancer_type,
        selected_factor=factor
    )
