from flask import Flask, render_template, request
from ..db.db_connector import get_db_connection
from ..db.queries import *
import os

# Define absolute paths for templates and static folders
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, '../../templates')
static_dir = os.path.join(base_dir, '../../static')

# Initialize Flask app with absolute paths for templates and static files
app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)

@app.route('/heatmap', methods=['GET', 'POST'])
def heatmap():
    data = None
    cancer_type = None
    year = None
    is_female = None
    is_alive = None
    race_id = None

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
        is_alive_options=is_alive_options
    )



if __name__ == "__main__":
    app.run(debug=True)
