from flask import Blueprint, render_template, request
from ..db.db_connector import get_db_connection
from ..db.insights_queries import *
import pandas as pd
import plotly.graph_objects as go

# Define the Blueprint
insights_bp = Blueprint('insights', __name__, template_folder='../../templates')

@insights_bp.route('/insights', methods=['GET'])
def insights():

    # Get database connection and cursor
    conn, cursor = get_db_connection()

    try:
        # Execute the query
        query = income_vs_mortality()
        cursor.execute(query)
        data = cursor.fetchall()
    finally:
        # Ensure resources are properly closed
        cursor.close()
        conn.close()

    # Convert results to DataFrame for easier manipulation
    df = pd.DataFrame(data, columns=['state', 'median_income', 'mortality_rate'])

    # Generate a scatter plot
    scatter_plot = go.Figure()
    scatter_plot.add_trace(
        go.Scatter(
            x=df['median_income'],
            y=df['mortality_rate'],
            mode='markers',
            marker=dict(size=10, color='blue'),
            text=df['state'],  # Tooltip text
            name="Income vs Mortality"
        )
    )
    scatter_plot.update_layout(
        title="Income vs Cancer Mortality Rate by State",
        xaxis_title="Median Income",
        yaxis_title="Mortality Rate",
        height=600,
        width=800,
    )

    # Render the Insights page with the chart and data
    return render_template(
        'insights.html',
        plot_html=scatter_plot.to_html(full_html=False),
        data=data
    )
