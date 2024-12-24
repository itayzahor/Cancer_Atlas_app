def fetch_heatmap_data(cursor, cancer_type, year):
    query = """
    SELECT state_id, SUM(count) AS total_count
    FROM cancer_data
    JOIN sites ON cancer_data.site_id = sites.site_id
    WHERE sites.site_name = %s AND year = %s
    GROUP BY state_id;
    """
    cursor.execute(query, (cancer_type, year))
    return cursor.fetchall()


def fetch_sites(cursor):
    query = "SELECT site_name FROM sites ORDER BY site_name;"
    cursor.execute(query)
    return [row['site_name'] for row in cursor.fetchall()]


