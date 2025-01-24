def construct_heatmap_query(cancer_type, year, is_female, is_alive, race_id,
                            unemployement_min, unemployement_max, median_min,
                            median_max, insurance_min, insurance_max,
                            inactivity_min, inactivity_max, cigarette_min,
                            cigarette_max, aqi_min, aqi_max, co2_min, co2_max):
    """
    Constructs the heatmap query dynamically with the given filters.

    Args:
        cursor: Database cursor for executing queries.

    Fields for Filtering:
        - cancer_type (str): ID of the cancer type to filter by. Use "-" for no filter.
        - year (str): Year to filter by. Use "-" for no filter.
        - is_female (str): Filter by gender (1 for female, 0 for male). Use "-" for no filter.
        - is_alive (str): Filter by survival status (1 for alive, 0 for deceased). Use "-" for no filter.
        - race_id (str): ID of the race to filter by. Use "-" for no filter.
        - unemployement_min (float): Minimum unemployment rate.
        - unemployement_max (float): Maximum unemployment rate.
        - median_min (int): Minimum median income.
        - median_max (int): Maximum median income.
        - insurance_min (float): Minimum insurance rate.
        - insurance_max (float): Maximum insurance rate.
        - inactivity_min (float): Minimum inactivity rate.
        - inactivity_max (float): Maximum inactivity rate.
        - cigarette_min (float): Minimum cigarette use rate.
        - cigarette_max (float): Maximum cigarette use rate.
        - aqi_min (float): Minimum air quality index.
        - aqi_max (float): Maximum air quality index.
        - co2_min (float): Minimum CO2 emissions.
        - co2_max (float): Maximum CO2 emissions.

    Returns:
        str: The fully constructed SQL query as a string.
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
            sd.median_income,
            e.air_quality_index,
            e.co2_emissions
        FROM states s
        LEFT JOIN cancer_data c ON s.id = c.state_id
    """
    params = []

    # Build filtering conditions dynamically for cancer_data before the join to execute the query faster These conditions are applied in the ON clause of the LEFT JOIN to filter rows early, reducing the number of rows processed in the join.
    if cancer_type != "-":
        query += f" AND c.cancer_type_id = {int(cancer_type)}"
    if year != "-":
        query += f" AND c.year = {int(year)}"
    if is_female != "-":
        query += f" AND c.is_female = {int(is_female)}"
    if is_alive != "-":
        query += f" AND c.is_alive = {int(is_alive)}"
    if race_id != "-":
        query += f" AND c.race_id = {int(race_id)}"


    # Add remaining joins to include related data from demographics, socioeconomic, risk factors, and environmental tables.
    query += """
        LEFT JOIN demographics d ON s.id = d.state_id
        LEFT JOIN socioeconomic_data sd ON s.id = sd.state_id
        LEFT JOIN risk_factors rf ON s.id = rf.state_id
        LEFT JOIN environmental e ON s.id = e.state_id
        WHERE 1=1
    """

    # Add filters for socioeconomic factors
    if unemployement_min is not None:
        query += f" AND sd.unemployment_rate >= {unemployement_min}"
    if unemployement_max is not None:
        query += f" AND sd.unemployment_rate <= {unemployement_max}"

    if median_min is not None:
        query += f" AND sd.median_income >= {median_min}"
    if median_max is not None:
        query += f" AND sd.median_income <= {median_max}"

    if insurance_min is not None:
        query += f" AND sd.insurance_rate >= {insurance_min}"
    if insurance_max is not None:
        query += f" AND sd.insurance_rate <= {insurance_max}"

    # Add filters for risk factors
    if inactivity_min is not None:
        query += f" AND rf.inactivity_rate >= {inactivity_min}"
    if inactivity_max is not None:
        query += f" AND rf.inactivity_rate <= {inactivity_max}"

    if cigarette_min is not None:
        query += f" AND rf.cigarette_use_rate >= {cigarette_min}"
    if cigarette_max is not None:
        query += f" AND rf.cigarette_use_rate <= {cigarette_max}"

    # Add filters for environmental factors
    if aqi_min is not None:
        query += f" AND e.air_quality_index >= {aqi_min}"
    if aqi_max is not None:
        query += f" AND e.air_quality_index <= {aqi_max}"

    if co2_min is not None:
        query += f" AND e.co2_emissions >= {co2_min}"
    if co2_max is not None:
        query += f" AND e.co2_emissions <= {co2_max}"

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
            sd.median_income,
            e.air_quality_index,
            e.co2_emissions;
    """

    return query


def fetch_cancer_types(cursor):
    query = "SELECT id, name FROM cancer_types ORDER BY name;"
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










