from flask import Blueprint, render_template

# Define the Blueprint
home_bp = Blueprint('home', __name__, template_folder='../templates')

# Define the route for the homepage
@home_bp.route('/cancer_atlas')
def homepage():
    return render_template('home.html')
