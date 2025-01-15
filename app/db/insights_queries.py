def socioeconomic_vs_mortality(cancer_type, factor):
    # Validate the factor to prevent SQL injection
    valid_factors = ["median_income", "unemployment_rate", "insurance_rate"]
    if factor not in valid_factors:
        raise ValueError(f"Invalid factor: {factor}")

    query = f"""
        SELECT 
            s.name AS state,
            se.{factor} AS socioeconomic_factor,
            mortality.mortality_rate AS mortality_rate
        FROM 
            (SELECT 
                c.state_id, 
                SUM(c.count) / NULLIF(SUM(d.total_population), 0) * 1000 AS mortality_rate
             FROM 
                cancer_data c
             JOIN 
                demographics d ON c.state_id = d.state_id
             WHERE 
                c.is_alive = 0
    """
    if cancer_type != "-":
        query += f" AND c.site_id = {int(cancer_type)}"

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
    # Validate the factor to prevent SQL injection
    valid_factors = ["cigarette_use_rate", "inactivity_rate"]
    if factor not in valid_factors:
        raise ValueError(f"Invalid factor: {factor}")

    query = f"""
        SELECT 
            s.name AS state,
            rf.{factor} AS risk_factor,
            incidence.incidence_rate AS cancer_incidence_rate
        FROM 
            (SELECT 
                c.state_id, 
                SUM(c.count) / NULLIF(SUM(d.total_population), 0) * 1000 AS incidence_rate
             FROM 
                cancer_data c
             JOIN 
                demographics d ON c.state_id = d.state_id
             WHERE 
                c.is_alive = 1  -- Only incidence data
    """
    if cancer_type != "-":
        query += f" AND c.site_id = {int(cancer_type)}"

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
    # Validate the factor to prevent SQL injection
    valid_factors = ["air_quality_index", "co2_emissions"]
    if factor not in valid_factors:
        raise ValueError(f"Invalid factor: {factor}")

    query = f"""
        SELECT 
            s.name AS state,
            e.{factor} AS environmental_factor,
            incidence.incidence_rate AS cancer_incidence_rate
        FROM 
            (SELECT 
                c.state_id,
                SUM(c.count) / NULLIF(SUM(d.total_population), 0) * 1000 AS incidence_rate
             FROM 
                cancer_data c
             JOIN 
                demographics d ON c.state_id = d.state_id
             WHERE 
                c.is_alive = 1  -- Only incidence data
    """
    if cancer_type != "-":
        query += f" AND c.site_id = {int(cancer_type)}"

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


