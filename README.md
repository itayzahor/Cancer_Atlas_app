# Cancer_Atlas_app

Our application, Cancer Atlas, is an interactive platform for exploring cancer statistics and their relationships with various factors, including socioeconomic, environmental, and behavioral risk factors in the United States. This guide will help you set up and run the application.

## Prerequisites
Before you begin, ensure that your computer has the following installed:

- Python 3
- pip (Python’s package manager)
- MySQL Server


# Installation Steps
**1. Clone the Repository**

Clone the repository to your local machine using the following command:

`git clone <https://github.com/itayzahor/Cancer_Atlas_app.git>`

**2. Create a Virtual Environment** (Optional)

Creating a virtual environment is recommended for managing dependencies. Run the following command:

`python -m venv venv`

**3. Activate the Virtual Environment** (Optional)

On Windows:

`.\venv\Scripts\activate`

On Linux or macOS:

`source venv/bin/activate`

**4. Install Required Libraries**

Install the necessary Python libraries by running:

`pip install -r requirements.txt`

If the installation fails, refer to the file:

`Python_libraries_installs.txt`

This file contains all the libraries downloaded for this project.



### Database Setup

Follow these steps to set up the database for the application:

**1. Start MySQL Server**  
   Ensure that the MySQL Server is running on your machine.

**2. Create the Database**  
   Open MySQL and run the following command to create the database:
   ```sql
   CREATE DATABASE cancer_atlas;
   ```

**3. Import Data**  
   - Open MySQL Workbench (or your preferred MySQL client).  
   - Click on **Server** → **Data Import**.  
   - Select the provided `data.sql` file from the repository and import it.

**4. Configure Database Connection**  
   - The application connects to MySQL using `db_connector.py`.  
   - Open `db_connector.py` and ensure the connection parameters match your MySQL setup:
     ```python
     db_config = {
         "host": "your_host",
         "user": "your_username",
         "password": "your_password",
         "database": "cancer_atlas"
     }
     ```

## Running the Application
Start the Flask application by running:
`python run.py`

Once the server is running, the application will be accessible at:
<http://127.0.0.1:5000/cancer_atlas>

## Troubleshooting

404 Error:
If you encounter a 404 error, ensure you are accessing the correct URL and that the application is running.

Database Connection Issues:
Verify that MySQL Server is active and the connection details in db_connector.py are correct (e.g the host, user, password and database) .








