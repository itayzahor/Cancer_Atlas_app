from app import create_app
from app.home import home_bp


# Create the Flask app
app = create_app()

app.register_blueprint(home_bp)

if __name__ == "__main__":
    # Run the app in debug mode for development
    app.run(debug=True)
