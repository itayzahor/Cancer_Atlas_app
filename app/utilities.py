from flask import Blueprint, Response, session, request

# Define a general Blueprint for shared utilities
utilities_bp = Blueprint('utilities', __name__)

@utilities_bp.route('/download_csv', methods=['GET'])
def download_csv():
    # Get the session key from the query parameter
    data_key = request.args.get('data_key')
    if not data_key:
        return "No data key provided.", 400

    # Retrieve data from the session
    data = session.get(data_key, [])
    if not data:
        return f"No data available to download for key: {data_key}.", 400

    # Generate the CSV file
    def generate():
        if not data:
            yield "No data available\n"
            return
        header = data[0].keys()
        yield ','.join(header) + '\n'
        for row in data:
            yield ','.join([str(row[key]) for key in header]) + '\n'

    # Create the response
    response = Response(generate(), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename={data_key}.csv'
    return response


