from .queries import *
from .insights_queries import *
from .db_connector import *

def get_cancer_types():
    """
    Fetches cancer types and ensures 'All Cancer Types' is always the first option.
    Returns None if the query fails.
    """
    query_result = execute_query(fetch_cancer_types_query)
    if query_result is None:
        return None  # Return None if there was an error in the query
    return [{'id': '-', 'name': 'All Cancer Types'}] + query_result

def get_races():
    """
    Fetches race options and ensures 'All Races' is always the first option.
    Returns None if the query fails.
    """
    query_result = execute_query(fetch_races_query)
    if query_result is None:
        return None  # Return None if there was an error in the query
    return [{'id': '-', 'name': 'All Races'}] + query_result


def get_years():
    """
    Fetches years and ensures 'All Years' is always the first option.
    Returns None if the query fails.
    """
    query_result = execute_query(fetch_years_query)
    if query_result is None:
        return None  # Return None if there was an error in the query
    # Transform years into the expected format
    return [{'year': '-', 'name': 'All Years'}] + [{'year': row['year'], 'name': row['year']} for row in query_result]

def fetch_heatmap_data(cancer_type, year, is_female, is_alive, race_id,
                       unemployement_min, unemployement_max, median_min, median_max,
                       insurance_min, insurance_max, inactivity_min, inactivity_max,
                       cigarette_min, cigarette_max, aqi_min, aqi_max, co2_min, co2_max):
    """
    Fetches heatmap data based on the provided filters.

    Args:
        cancer_type: Filter for cancer type.
        year: Year to filter by.
        is_female: Gender filter.
        is_alive: Survival status filter.
        race_id: Race filter.
        unemployement_min: Minimum unemployment rate.
        unemployement_max: Maximum unemployment rate.
        median_min: Minimum median income.
        median_max: Maximum median income.
        insurance_min: Minimum insurance rate.
        insurance_max: Maximum insurance rate.
        inactivity_min: Minimum inactivity rate.
        inactivity_max: Maximum inactivity rate.
        cigarette_min: Minimum cigarette use rate.
        cigarette_max: Maximum cigarette use rate.
        aqi_min: Minimum air quality index.
        aqi_max: Maximum air quality index.
        co2_min: Minimum CO2 emissions.
        co2_max: Maximum CO2 emissions.

    Returns:
        list[dict] or None: The heatmap data or None if an error occurs.
    """
    return execute_query(
        construct_heatmap_query,
        cancer_type, year, is_female, is_alive, race_id,
        unemployement_min, unemployement_max, median_min, median_max,
        insurance_min, insurance_max, inactivity_min, inactivity_max,
        cigarette_min, cigarette_max, aqi_min, aqi_max, co2_min, co2_max
    )

def fetch_environmental_vs_incidence(cancer_type, factor):
    """
    Fetches data for the relationship between the selected cancer type and an environmental factor.

    Args:
        cancer_type (str): The selected cancer type.
        factor (str): The environmental factor to analyze.

    Returns:
        list[dict] or None: The queried data, or None if an error occurs.
    """
    return execute_query(environmental_vs_incidence, cancer_type, factor)

def fetch_risk_factors_vs_incidence(cancer_type, factor):
    """
    Fetches data for the relationship between the selected cancer type and a risk factor.

    Args:
        cancer_type (str): The selected cancer type.
        factor (str): The risk factor to analyze.

    Returns:
        list[dict] or None: The queried data, or None if an error occurs.
    """
    return execute_query(risk_factors_vs_incidence, cancer_type, factor)

def fetch_socioeconomic_vs_mortality(cancer_type, factor):
    """
    Fetches data for the relationship between the selected cancer type and a socioeconomic factor.

    Args:
        cancer_type (str): The selected cancer type.
        factor (str): The socioeconomic factor to analyze.

    Returns:
        list[dict] or None: The queried data, or None if an error occurs.
    """
    return execute_query(socioeconomic_vs_mortality, cancer_type, factor)