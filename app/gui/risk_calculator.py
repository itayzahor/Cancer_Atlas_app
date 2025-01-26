from flask import Blueprint, render_template, request
from app.db.db_connector import get_db_connection

risk_calculator_bp = Blueprint('risk_calculator', __name__, template_folder='../../templates')

@risk_calculator_bp.route('/risk_calculator', methods=['GET', 'POST'])
def risk_calculator():
    risk_result = None  # Initialize risk result variable
    if request.method == 'POST':
        # Get form data
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        smoking = request.form.get('smoking')
        family_history = request.form.get('family_history')

        # Basic risk calculation logic
        risk_score = 0

        # Age factor
        if age < 30:
            risk_score += 1
        elif 30 <= age < 50:
            risk_score += 2
        else:
            risk_score += 3

        # Gender factor
        if gender == 'male':
            risk_score += 2  # Higher risk for males
        else:
            risk_score += 1  # Lower risk for females

        # Smoking factor
        if smoking == 'yes':
            risk_score += 3  # Significant risk increase for smokers

        # Family history factor
        if family_history == 'yes':
            risk_score += 2  # Increased risk if there's a family history

        # Determine risk level based on score
        if risk_score <= 3:
            risk_result = "Low Risk"
        elif 4 <= risk_score <= 6:
            risk_result = "Moderate Risk"
        else:
            risk_result = "High Risk"

    return render_template('risk_calculator.html', risk_result=risk_result) 