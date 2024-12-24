# app/__init__.py

# This makes the `db_connector` and `queries` available for easy imports.
from app.db.db_connector import get_db_connection
from app.db.queries import fetch_heatmap_data
