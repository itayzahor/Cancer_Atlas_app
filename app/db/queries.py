def fetch_heatmap_data(cursor, cancer_type, year, is_female, is_alive, race_id):
    """
    Fetch heatmap data including population data for calculating rates.

    Args:
        cursor: Database cursor for executing queries.
        cancer_type: Filter by cancer type.
        year: Filter by year.
        is_female: Filter by gender (1 for female, 0 for male, "-" for all).
        is_alive: Filter by survival status (1 for alive, 0 for deceased, "-" for all).
        race_id: Filter by race ("-" for all).

    Returns:
        list of dict: Data for generating the heatmap.
    """
    query = """
        SELECT 
            d.state_id,
            COALESCE(cd.total_count, 0) AS total_count,
            d.total_population,
            d.male_population,
            d.female_population,
            d.white_population,
            d.black_population,
            d.asian_population,
            d.hispanic_population,
            d.native_pacific_population,
            s.abbreviation,
            s.latitude,
            s.longitude,
            s.name
        FROM demographics d
        LEFT JOIN (
            SELECT 
                state_id,
                SUM(count) AS total_count
            FROM cancer_data
            WHERE 1=1
    """

    params = []

    # Add filters for cancer_data subquery
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

    query += """
            GROUP BY state_id
        ) cd ON d.state_id = cd.state_id
        LEFT JOIN states s ON d.state_id = s.id
    """

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







