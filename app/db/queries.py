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
            COALESCE(SUM(c.count), 0) AS total_count,
            d.total_population,
            d.male_population,
            d.female_population,
            d.white_population,
            d.black_population,
            d.asian_population,
            d.hispanic_population,
            d.native_pacific_population
        FROM demographics d
        LEFT JOIN cancer_data c ON d.state_id = c.state_id
    """
    
    on_clauses = []
    params = []

    # Add filters to the LEFT JOIN ON clause
    if cancer_type != "-":
        on_clauses.append("c.site_id = %s")
        params.append(int(cancer_type))
    if year != "-":
        on_clauses.append("c.year = %s")
        params.append(int(year))
    if is_female != "-":
        on_clauses.append("c.is_female = %s")
        params.append(int(is_female))
    if is_alive != "-":
        on_clauses.append("c.is_alive = %s")
        params.append(int(is_alive))
    if race_id != "-":
        on_clauses.append("c.race_id = %s")
        params.append(int(race_id))

    # Add ON clause filters
    if on_clauses:
        query += " AND " + " AND ".join(on_clauses)

    query += """
    GROUP BY 
        d.state_id, 
        d.total_population, 
        d.male_population, 
        d.female_population, 
        d.white_population, 
        d.black_population, 
        d.asian_population, 
        d.hispanic_population, 
        d.native_pacific_population
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







