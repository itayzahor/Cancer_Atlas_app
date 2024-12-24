from flask import Flask, render_template, request
from ..db.db_connector import get_db_connection
from ..db.queries import fetch_heatmap_data, fetch_sites
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

    conn, cursor = get_db_connection()
    cancer_types = fetch_sites(cursor)  # Fetch cancer types for dropdown
    cursor.close()
    conn.close()

    if request.method == 'POST':
        # Get user inputs from the form
        cancer_type = request.form.get('cancer_type')
        year = request.form.get('year')

        # Fetch data from the database
        conn, cursor = get_db_connection()
        data = fetch_heatmap_data(cursor, cancer_type, year)
        cursor.close()
        conn.close()

    # Render the template with the data and cancer types
    return render_template('heatmap.html', data=data, cancer_type=cancer_type, year=year, cancer_types=cancer_types)


if __name__ == "__main__":
    app.run(debug=True)
