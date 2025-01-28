def socioeconomic_vs_mortality(cancer_type, factor):
    """
    Constructs a SQL query to analyze the relationship between cancer mortality rates
    and a specified socioeconomic factor for each state.

    Parameters:
        cancer_type (str): The type of cancer to filter by. Use "-" to include all cancer types.
        factor (str): The socioeconomic factor to analyze. Must correspond to a valid column 
                      in the "socioeconomic_data" table (e.g., 'median_income', 'unemployment_rate').

    Returns:
        str: A SQL query string that retrieves the following:
             - State name (s.name)
             - Socioeconomic factor value (se.{factor})
             - Cancer mortality rate per 100 people (calculated as:
               SUM(c.count) / total_population * 100)
    
    Query Details:
        - The inner query calculates the cancer mortality rate for each state by dividing the total cancer deaths (SUM(c.count)) by the total population (d.total_population), multiplied by 100 to express as a percentage.
        - If a specific cancer type is provided (cancer_type != "-"), the query filters cases based on the `cancer_type_id`.
        - The outer query joins the calculated mortality rates with state names 
          (from the `states` table) and socioeconomic factor data (from the `socioeconomic_data` table).
    """
    query = f"""
        SELECT 
            s.name AS state,
            se.{factor} AS socioeconomic_factor,
            mortality.mortality_rate AS mortality_rate
        FROM 
            (SELECT 
                c.state_id,
                SUM(c.count) / NULLIF(d.total_population, 0) * 100 AS mortality_rate
             FROM 
                cancer_data c
             JOIN 
                demographics d ON c.state_id = d.state_id
             WHERE 
                c.is_alive = 0  -- Only mortality data
    """
    if cancer_type != "-":
        query += f" AND c.cancer_type_id = {int(cancer_type)}"

    query += f"""
             GROUP BY c.state_id
            ) AS mortality
        JOIN 
            states s ON mortality.state_id = s.id
        JOIN 
            socioeconomic_data se ON mortality.state_id = se.state_id
        GROUP BY s.name, se.{factor}, mortality.mortality_rate
    """
    return query

def risk_factors_vs_incidence(cancer_type, factor):
    """
    Constructs a SQL query to analyze the relationship between cancer incidence rates
    and a specified risk factor for each state.

    Parameters:
        cancer_type (str): The type of cancer to filter by. Use "-" to include all cancer types.
        factor (str): The risk factor to analyze. Must correspond to a valid column 
                      in the "risk_factors" table (e.g., 'inactivity_rate', 'cigarette_use_rate').

    Returns:
        str: A SQL query string that retrieves the following:
             - State name (s.name)
             - Risk factor value (rf.{factor})
             - Cancer incidence rate per 100 people (calculated as:
               SUM(c.count) / total_population * 100)
    
    Query Details:
        - The inner query calculates the cancer incidence rate for each state by dividing the total cancer cases (SUM(c.count)) by the total population (d.total_population), multiplied by 100 to express as a percentage.
        - If a specific cancer type is provided (cancer_type != "-"), the query filters cases based on the `cancer_type_id`.
        - The outer query joins the calculated incidence rates with state names 
          (from the `states` table) and risk factor data (from the `risk_factors` table).
    """

    query = f"""
        SELECT 
            s.name AS state,
            rf.{factor} AS risk_factor,
            incidence.incidence_rate AS cancer_incidence_rate
        FROM 
            (SELECT 
                c.state_id,
                SUM(c.count) / NULLIF(d.total_population, 0) * 100 AS incidence_rate
             FROM 
                cancer_data c
             JOIN 
                demographics d ON c.state_id = d.state_id
             WHERE 
                c.is_alive = 1  -- Only incidence data
    """
    if cancer_type != "-":
        query += f" AND c.cancer_type_id = {int(cancer_type)}"

    query += f"""
             GROUP BY c.state_id
            ) AS incidence
        JOIN 
            states s ON incidence.state_id = s.id
        JOIN 
            risk_factors rf ON incidence.state_id = rf.state_id
        GROUP BY s.name, rf.{factor}, incidence.incidence_rate
    """
    return query


def environmental_vs_incidence(cancer_type, factor):
    """
    Constructs a SQL query to analyze the relationship between cancer incidence rates
    and a specified environmental factor for each state.

    Parameters:
        cancer_type (str): The type of cancer to filter by. Use "-" to include all cancer types.
        factor (str): The environmental factor to analyze. Must correspond to a valid column 
                      in the "environmental" table (e.g., 'air_quality_index', 'co2_emissions').

    Returns:
        str: A SQL query string that retrieves the following:
             - State name (s.name)
             - Environmental factor value (e.{factor})
             - Cancer incidence rate per 100 people (calculated as:
               SUM(c.count) / total_population * 100)
    
    Query Details:
        - The inner query calculates the cancer incidence rate for each state by dividing the total cancer cases (SUM(c.count)) by the total population (d.total_population), multiplied by 100 to express as a percentage.
        - If a specific cancer type is provided (cancer_type != "-"), the query filters cases based on the `cancer_type_id`.
        - The outer query joins the calculated incidence rates with state names 
          (from the `states` table) and environmental factor data (from the `environmental` table).
        
    """

    query = f"""
        SELECT 
            s.name AS state,
            e.{factor} AS environmental_factor,
            incidence.incidence_rate AS cancer_incidence_rate
        FROM 
            (SELECT 
                c.state_id,
                SUM(c.count) / NULLIF(d.total_population, 0) * 100 AS incidence_rate
             FROM 
                cancer_data c
             JOIN 
                demographics d ON c.state_id = d.state_id
             WHERE 
                c.is_alive = 1  -- Only incidence data
    """
    if cancer_type != "-":
        query += f" AND c.cancer_type_id = {int(cancer_type)}"

    query += f"""
             GROUP BY c.state_id
            ) AS incidence
        JOIN 
            states s ON incidence.state_id = s.id
        JOIN 
            environmental e ON incidence.state_id = e.state_id
        GROUP BY s.name, e.{factor}, incidence.incidence_rate
    """
    return query


