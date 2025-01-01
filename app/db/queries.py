def fetch_heatmap_data(cursor, cancer_type, year, is_female, is_alive, race_id):
    query = """
    SELECT state_id, SUM(count) AS total_count
    FROM cancer_data
    WHERE 1=1
    """
    params = []

    # Add conditions dynamically, skipping filters for "All" (`"-"`)
    if cancer_type != "-":
        query += " AND site_id = %s"
        params.append(int(cancer_type))
    if year != "-":
        query += " AND year = %s"
        params.append(int(year))
    if is_female != "-":
        query += " AND is_female = %s"
        params.append(int(is_female))
    if is_alive != "-":
        query += " AND is_alive = %s"
        params.append(int(is_alive))
    if race_id != "-":
        query += " AND race_id = %s"
        params.append(int(race_id))

    query += " GROUP BY state_id"

    # Execute the query
    cursor.execute(query, params)
    return cursor.fetchall()


def fetch_sites(cursor):
    query = "SELECT id, name FROM sites ORDER BY name;"
    cursor.execute(query)
    return cursor.fetchall()


def fetch_races(cursor):
    query = "SELECT id, name FROM races ORDER BY name;"
    cursor.execute(query)
    return cursor.fetchall()

def fetch_years(cursor):
    query = "SELECT DISTINCT year FROM cancer_data ORDER BY year;"
    cursor.execute(query)
    return [row['year'] for row in cursor.fetchall()]





