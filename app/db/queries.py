def construct_heatmap_query(cancer_type, year, is_female, is_alive, race_id,
                            unemployement_min, unemployement_max, median_min,
                            median_max, insurance_min, insurance_max,
                            inactivity_min, inactivity_max, cigarette_min,
                            cigarette_max, aqi_min, aqi_max, co2_min, co2_max):
    """
    this function constructs a SQL query to fetch data for the heatmap based on the provided filters. Afterwards it calculates the filtered population and rate according to the filter. Finally, it normalizes the rate for easier comparison in the heatmap. All in all, this function returns a query that calculates all the data needed for the heatmap in the the db itself, instead of doing the calculations in the app.


    Args:
        cancer_type: Filter for cancer type.
        year: Year to filter by.
        is_female: Gender filter.
        is_alive: Survival status filter.
        race_id: Race filter.
        unemployement_min, unemployement_max: Range for unemployment rate.
        median_min, median_max: Range for median income.
        insurance_min, insurance_max: Range for insurance rate.
        inactivity_min, inactivity_max: Range for inactivity rate.
        cigarette_min, cigarette_max: Range for cigarette use rate.
        aqi_min, aqi_max: Range for air quality index.
        co2_min, co2_max: Range for CO2 emissions.

    Returns:
        str: The fully constructed SQL query as a string, including:
             - Filtered population
             - Calculated cancer rates
             - Normalized rates for easier comparison
    """

    # Add filtered population logic dynamically
    if race_id == 1:
        race_population = "d.native_pacific_population"
    elif race_id == 2:
        race_population = "d.black_population"
    elif race_id == 3:
        race_population = "d.hispanic_population"
    elif race_id == 4:
        race_population = "d.asian_population"
    elif race_id == 5:
        race_population = "d.white_population"
    else:
        race_population = "d.total_population"

    # Add gender-specific adjustments dynamically
    if is_female == "1":
        filtered_population = f"{race_population} * (d.female_population / NULLIF(d.total_population, 0))"
    elif is_female == "0":
        filtered_population = f"{race_population} * (d.male_population / NULLIF(d.total_population, 0))"
    else:
        filtered_population = race_population

    
    query = f"""
        WITH base_data AS (
            SELECT 
                s.name,
                s.abbreviation,
                s.latitude,
                s.longitude,
                COALESCE(SUM(c.count), 0) AS total_count,
                {filtered_population} AS filtered_population
            FROM states s
            LEFT JOIN cancer_data c ON s.id = c.state_id
    """
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
            s.id
        ),
        """

    # Add rate calculation logic 
    # When calculating the rate, we check for division by zero to avoid errors
    # We also round the rate to 2 decimal places
    query += """
        rate_data AS (
        SELECT
            base_data.*,
            -- Calculate rate using precomputed filtered_population
            ROUND(
                CASE
                    WHEN total_count > 0 AND filtered_population > 0 THEN
                        (total_count / filtered_population) * 100
                    ELSE 0
                END, 2
            ) AS rate
        FROM base_data
    ),
    """

    # Add the final query to fetch the data and normalize the rate
    query += """
        final_data AS (
            SELECT 
                rate_data.*,
                CASE 
                    WHEN rate_bounds.max_rate > rate_bounds.min_rate THEN 
                        (rate_data.rate - rate_bounds.min_rate) / (rate_bounds.max_rate - rate_bounds.min_rate)
                    ELSE 0
                END AS normalized_rate
            FROM rate_data,
                (SELECT MIN(rate) AS min_rate, MAX(rate) AS max_rate FROM rate_data) AS rate_bounds
        )
        SELECT * FROM final_data;
    """
    return query


def fetch_cancer_types_query():
    """
    Returns the SQL query to fetch all the different cancer types.
    """
    return "SELECT id, name FROM cancer_types ORDER BY name;"


def fetch_races_query():
    """
    Returns the SQL query to fetch all the different races.
    """
    return "SELECT id, name FROM races ORDER BY name;"


def fetch_years_query():
    """
    Returns the SQL query to fetch distinct years from cancer_data.
    """
    return "SELECT DISTINCT year FROM cancer_data ORDER BY year;"










