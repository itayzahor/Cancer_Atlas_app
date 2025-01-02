from flask import Flask, render_template, request
from ..db.db_connector import get_db_connection
from ..db.queries import *
import os
import plotly.graph_objects as go
import pandas as pd

# Define absolute paths for templates and static folders
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, '../../templates')
static_dir = os.path.join(base_dir, '../../static')

# Initialize Flask app with absolute paths for templates and static files
app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)

def calculate_rates(data, filters):
    """
    Calculate rates (as percentages), normalized rates, and assign colors for the heatmap.

    Args:
        data (list of dict): Raw data from the query.
        filters (dict): User-selected filters (e.g., gender_id, race_id).

    Returns:
        list of dict: Data with additional columns for filtered population, rates, normalized rates, and colors.
    """
    rates = []
    min_rate, max_rate = float('inf'), float('-inf')

    for row in data:
        # Convert populations to floats for safe division
        total_population = float(row['total_population'])
        female_population = float(row['female_population'])
        male_population = float(row['male_population'])
        race_population = 0

        # Determine the race-specific population
        if filters['race_id'] == 1:  # American Indian/Alaska Native, Non-Hispanic
            race_population = float(row.get('native_pacific_population', 0))
        elif filters['race_id'] == 2:  # Black, Non-Hispanic
            race_population = float(row.get('black_population', 0))
        elif filters['race_id'] == 3:  # Hispanic
            race_population = float(row.get('hispanic_population', 0))
        elif filters['race_id'] == 4:  # Non-Hispanic Asian/Pacific Islander
            race_population = float(row.get('asian_population', 0))
        elif filters['race_id'] == 5:  # Non-Hispanic White
            race_population = float(row.get('white_population', 0))
        else:  # All races
            race_population = total_population

        # Combine race population with gender-specific population
        if filters['gender_id'] == "1":  # Female
            filtered_population = race_population * (female_population / total_population)
        elif filters['gender_id'] == "0":  # Male
            filtered_population = race_population * (male_population / total_population)
        else:  # All genders
            filtered_population = race_population

        # Round the filtered population to avoid decimals
        filtered_population = round(filtered_population)

        # Add the filtered population to the row
        row['filtered_population'] = filtered_population

        if row['total_count'] > 0 and filtered_population > 0:
            rate = (row['total_count'] / filtered_population) * 100
            min_rate = min(min_rate, rate)
            max_rate = max(max_rate, rate)
        else:
            rate = 0


        # Append the rate to the row
        row['rate'] = round(rate, 2)
        rates.append(row)

    # Round min_rate and max_rate to 2 decimal places for consistency
    min_rate = round(min_rate, 2)
    max_rate = round(max_rate, 2)


    # Normalize rates (0–1) and assign colors
    for row in rates:
        if max_rate > min_rate and row['total_count'] > 0:  # Avoid division by zero
            row['normalized_rate'] = round(
            (row['rate'] - min_rate) / (max_rate - min_rate), 2)
        else:
            row['normalized_rate'] = 0

    return rates



@app.route('/heatmap', methods=['GET', 'POST'])
def heatmap():
    data = None
    cancer_type = None
    year = None
    is_female = None
    is_alive = None
    race_id = None
    heatmap_html = None

    # Fetch options for dropdowns
    conn, cursor = get_db_connection()
    cancer_types = fetch_sites(cursor)
    races = fetch_races(cursor)
    years = fetch_years(cursor)
    cursor.close()
    conn.close()

    if request.method == 'POST':
        # Get user inputs from the form
        cancer_type = request.form.get('cancer_type', "-")
        year = request.form.get('year', "-")
        is_female = request.form.get('is_female', "-")
        is_alive = request.form.get('is_alive', "-")
        race_id = request.form.get('race_id', "-")

        # Convert to integers if not "All" (`"-"`)
        cancer_type = int(cancer_type) if cancer_type != "-" else "-"
        race_id = int(race_id) if race_id != "-" else "-"
        year = int(year) if year != "-" else "-"

        # Fetch data from the database
        conn, cursor = get_db_connection()
        data = fetch_heatmap_data(cursor, cancer_type, year, is_female, is_alive, race_id)
        cursor.close()
        conn.close()

        # Apply rate calculations
        filters = {
            "gender_id": is_female,
            "race_id": race_id,
        }
        data = calculate_rates(data, filters)

       # Prepare data for the heatmap
        df = pd.DataFrame(data)

        # Add a hover text column for custom display
        df['hover_text'] = df.apply(
            lambda row: f"{row['name']}<br>Rate: {row['rate']}%", axis=1
        )

        # Create the Choropleth map
        fig = go.Figure()

        # Add Choropleth layer
        fig.add_trace(go.Choropleth(
            locations=df['abbreviation'],  # Use state abbreviations for mapping
            z=df['normalized_rate'],  # Normalized rates for coloring
            locationmode='USA-states',  # Match state abbreviations to US states
            colorscale="Reds",  # Use a predefined colorscale
            showscale=True,  # Display the color bar
            colorbar=dict(title="Normalized Rate"),  # Title for the color bar
            text=df['hover_text'],  # Custom hover text
            hoverinfo='text',  # Display only the custom hover text
        ))

        # Update layout
        fig.update_layout(
            geo=dict(
                scope='usa',  # Focus on US
                showlakes=True,  # Show lakes
                lakecolor='rgb(255, 255, 255)',  # Color for lakes
            ),
            title_text='US Heatmap by State (Normalized Rates)',
            width=1200,  # Increase map width
            height=800,  # Increase map height
        )

        # Convert Plotly figure to HTML
        heatmap_html = fig.to_html(full_html=False)




    # Options for dropdowns
    is_female_options = [{'value': '1', 'label': 'Female'}, {'value': '0', 'label': 'Male'}]
    is_alive_options = [{'value': '1', 'label': 'Incidence'}, {'value': '0', 'label': 'Mortality'}]    

    # Render the template with data and dropdown options
    return render_template(
        'heatmap.html',
        data=data,
        cancer_type=cancer_type,
        year=year,
        years=years,
        cancer_types=cancer_types,
        is_female=is_female,
        is_alive=is_alive,
        race_id=race_id,
        races=races,
        is_female_options=is_female_options,
        is_alive_options=is_alive_options,
        heatmap_html=heatmap_html
    )



if __name__ == "__main__":
    app.run(debug=True)
