def income_vs_mortality():
    query = """
        SELECT 
            s.name AS state,
            se.median_income,
            mortality.mortality_rate
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
             GROUP BY c.state_id
            ) AS mortality
        JOIN 
            states s ON mortality.state_id = s.id
        JOIN 
            socioeconomic_data se ON mortality.state_id = se.state_id
    """
    query += " GROUP BY s.name, se.median_income, mortality.mortality_rate"
    return query
