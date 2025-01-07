def fetch_heatmap_data(cursor, cancer_type, year, is_female, is_alive, race_id, unemployement_min, unemployement_max, median_min, median_max):
    """
    Fetch heatmap data including population, cancer cases, and socioeconomic data,
    with a custom unemployment rate range.

    Args:
        cursor: Database cursor for executing queries.
        cancer_type (str): Filter by cancer type. Use "-" for no filter.
        year (str): Filter by year. Use "-" for no filter.
        is_female (str): Filter by gender. Use "-" for no filter.
        is_alive (str): Filter by survival status. Use "-" for no filter.
        race_id (str): Filter by race. Use "-" for no filter.
        min_rate (float): Minimum unemployment rate for filtering.
        max_rate (float): Maximum unemployment rate for filtering.

    Returns:
        list of dict: Each dictionary contains state metadata, demographic data,
                      cancer data, and socioeconomic data.
    """
    query = """
        SELECT 
            s.name,
            s.abbreviation,
            s.latitude,
            s.longitude,
            COALESCE(SUM(c.count), 0) AS total_count,
            d.total_population,
            d.male_population,
            d.female_population,
            d.white_population,
            d.black_population,
            d.asian_population,
            d.hispanic_population,
            d.native_pacific_population,
            sd.unemployment_rate,
            sd.median_income
        FROM states s
        LEFT JOIN demographics d ON s.id = d.state_id
        LEFT JOIN cancer_data c ON d.state_id = c.state_id
        LEFT JOIN socioeconomic_data sd ON s.id = sd.state_id
        WHERE 1=1
    """

    params = []

    # Add filters dynamically
    if cancer_type != "-":
        query += " AND c.site_id = %s"
        params.append(int(cancer_type))
    if year != "-":
        query += " AND c.year = %s"
        params.append(int(year))
    if is_female != "-":
        query += " AND c.is_female = %s"
        params.append(int(is_female))
    if is_alive != "-":
        query += " AND c.is_alive = %s"
        params.append(int(is_alive))
    if race_id != "-":
        query += " AND c.race_id = %s"
        params.append(int(race_id))

    # Add unemployment rate filter
    if unemployement_min is not None and unemployement_max is not None:
        query += " AND sd.unemployment_rate BETWEEN %s AND %s"
        params.extend([unemployement_min , unemployement_max])

    # Add median income filter
    if median_min is not None and median_max is not None:
        query += " AND sd.median_income BETWEEN %s AND %s"
        params.extend([median_min, median_max])

    query += """
        GROUP BY 
            s.id,
            d.total_population,
            d.male_population,
            d.female_population,
            d.white_population,
            d.black_population,
            d.asian_population,
            d.hispanic_population,
            d.native_pacific_population,
            sd.unemployment_rate,
            sd.median_income;
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










