from flask import Blueprint, render_template, request, session
from ..db.db_connector import get_db_connection
from ..db.queries import *
import os
import plotly.graph_objects as go
import pandas as pd

# Define absolute paths for templates and static folders
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, '../../templates')
static_dir = os.path.join(base_dir, '../../static')

heatmap_bp = Blueprint('heatmap', __name__, template_folder='../../templates', static_folder='../../static')


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
        if filters['race_id'] == 1:  
            race_population = float(row.get('native_pacific_population', 0))
        elif filters['race_id'] == 2:  
            race_population = float(row.get('black_population', 0))
        elif filters['race_id'] == 3: 
            race_population = float(row.get('hispanic_population', 0))
        elif filters['race_id'] == 4:  
            race_population = float(row.get('asian_population', 0))
        elif filters['race_id'] == 5: 
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

@heatmap_bp.route('/', methods=['GET'])
def heatmap():
    show_advanced = request.args.get('show_advanced', 'false')

    data = []
    stats = {}
    heatmap_html = None

    # Fetch options for dropdowns
    conn, cursor = get_db_connection()
    cancer_types = fetch_sites(cursor)
    races = fetch_races(cursor)
    years = fetch_years(cursor)
    cursor.close()
    conn.close()

    # Get user inputs from the query string
    cancer_type = request.args.get('cancer_type', "-")
    year = request.args.get('year', "-")
    is_female = request.args.get('is_female', "-")
    is_alive = request.args.get('is_alive', "-")
    race_id = request.args.get('race_id', "-")
    unemployement_min = request.args.get('unemployement_min')
    unemployement_max = request.args.get('unemployement_max')
    median_min = request.args.get('median_min')
    median_max = request.args.get('median_max')
    insurance_min = request.args.get('insurance_min')
    insurance_max = request.args.get('insurance_max')
    inactivity_min = request.args.get('inactivity_min')
    inactivity_max = request.args.get('inactivity_max')
    cigarette_min = request.args.get('cigarette_min')
    cigarette_max = request.args.get('cigarette_max')
    aqi_min = request.args.get('aqi_min')
    aqi_max = request.args.get('aqi_max')
    co2_min = request.args.get('co2_min')
    co2_max = request.args.get('co2_max')

    # Convert form inputs to proper data types
    unemployement_min = float(unemployement_min) if unemployement_min else None
    unemployement_max = float(unemployement_max) if unemployement_max else None
    median_min = int(median_min) if median_min else None
    median_max = int(median_max) if median_max else None
    insurance_min = float(insurance_min) if insurance_min else None
    insurance_max = float(insurance_max) if insurance_max else None
    inactivity_min = float(inactivity_min) if inactivity_min else None
    inactivity_max = float(inactivity_max) if inactivity_max else None
    cigarette_min = float(cigarette_min) if cigarette_min else None
    cigarette_max = float(cigarette_max) if cigarette_max else None
    aqi_min = float(aqi_min) if aqi_min else None
    aqi_max = float(aqi_max) if aqi_max else None
    co2_min = float(co2_min) if co2_min else None
    co2_max = float(co2_max) if co2_max else None


    # Convert to integers if not "All" (`"-"`)
    cancer_type = int(cancer_type) if cancer_type != "-" else "-"
    race_id = int(race_id) if race_id != "-" else "-"
    year = int(year) if year != "-" else "-"

    try:
        conn, cursor = get_db_connection()
        data = fetch_heatmap_data(
            cursor, cancer_type, year, is_female, is_alive, race_id,
            unemployement_min, unemployement_max, median_min, median_max,
            insurance_min, insurance_max, inactivity_min, inactivity_max,
            cigarette_min, cigarette_max, aqi_min, aqi_max, co2_min, co2_max)
        
    except Exception as e:
        print(f"Database query failed: {e}")
        data = []  # Fallback to empty data
    finally:
        cursor.close()
        conn.close()

    # Apply rate calculations
    filters = {
        "gender_id": is_female,
        "race_id": race_id,
    }
    data = calculate_rates(data, filters)

            

    if data:
        # Calculate statistics
        total_cases = sum(row['total_count'] for row in data if row['total_count'])
        total_rates = sum(row['rate'] for row in data if row['rate'])
        avg_rate = round(total_rates / len(data), 2) if data else 0

        highest_rate = max(data, key=lambda row: row['rate'])
        lowest_rate = min(data, key=lambda row: row['rate'])

        stats = {
            'total_cases': total_cases,
            'avg_rate': avg_rate,
            'highest_rate': {
                'state': highest_rate['name'],
                'rate': highest_rate['rate']
            },
            'lowest_rate': {
                'state': lowest_rate['name'],
                'rate': lowest_rate['rate']
            }
        }

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
            ),
            title_text='US Heatmap by State (Normalized Rates)',
            width=1200,  # Increase map width
            height=600,  # Increase map height
        )


        # Convert Plotly figure to HTML
        heatmap_html = fig.to_html(full_html=False)

    else:
        stats = {
            'total_cases': 0,
            'avg_rate': 0,
            'highest_rate': {'state': 'N/A', 'rate': 'N/A'},
            'lowest_rate': {'state': 'N/A', 'rate': 'N/A'}
        }
        heatmap_html = None
    
    
    # Store the data directly in the session
    session['heatmap_data'] = data

    # Options for dropdowns
    is_female_options = [{'value': '1', 'label': 'Female'}, {'value': '0', 'label': 'Male'}]
    is_alive_options = [{'value': '1', 'label': 'New Cancer Cases'}, {'value': '0', 'label': 'Cancer-Related Deaths'}]    

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
        unemployement_min=unemployement_min,
        unemployement_max=unemployement_max,
        median_min=median_min,
        median_max=median_max,
        insurance_min=insurance_min,
        insurance_max=insurance_max,
        inactivity_min=inactivity_min,
        inactivity_max=inactivity_max,
        cigarette_min=cigarette_min,
        cigarette_max=cigarette_max,
        aqi_min=aqi_min,
        aqi_max=aqi_max,
        co2_min=co2_min,
        co2_max=co2_max,
        show_advanced=show_advanced,
        stats=stats,
        heatmap_html=heatmap_html
    )

