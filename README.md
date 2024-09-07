How to Run the Project Follow the steps below to set up and run the User Spending Dashboard project locally on your machine.

Clone the Repository First, clone the repository to your local machine using the following command:
bash Copy code git clone https://github.com/your-username/your-repo-name.git Navigate to the project directory:

bash Copy code cd your-repo-name 2. Set Up a Virtual Environment (Optional but Recommended) It's a good practice to create a virtual environment to manage your project dependencies.

On macOS/Linux:

bash Copy code python3 -m venv venv source venv/bin/activate On Windows:

bash Copy code python -m venv venv venv\Scripts\activate 3. Install the Required Libraries Once inside the project folder, install all the required dependencies using pip:

pip install -r requirements.txt This will install the following libraries:

Set Up the SQLite Database Ensure that the SQLite database (example.db) is created and populated with sample data. You can modify or add more data into the database as needed.
If example.db is missing, you can use the provided script in app.py to initialize the database with the required tables and sample data:

Open the app.py file. Look for the section that creates and inserts data into the database tables (users and transactions). Run the script once to generate the database file. bash Copy code python app.py 5. Run the Dash Application Start the Dash server by running the app.py file:

bash Copy code python app.py 6. Open the Dashboard in Your Browser Once the app is running, you will see output like:

Dash is running on http://127.0.0.1:8050/ Open your web browser and navigate to this URL:

![pic1](https://github.com/user-attachments/assets/3a06cf78-f1f0-4e62-a341-207eb40e55a3)
![pic2](https://github.com/user-attachments/assets/a9b5700a-8df1-4b74-bc1a-48cc75a09227)
![pic3](https://github.com/user-attachments/assets/8dac293c-898a-4f51-89dc-cd8732fdf220)
![pic4](https://github.com/user-attachments/assets/2e8a0160-8489-49ac-a012-75cd5318bf78)
![pic5](https://github.com/user-attachments/assets/0f625f97-1252-43c0-8e71-dd9521c4b05b)

Modify the Application (Optional) You can modify the following areas of the application:
Database Queries: Update or change SQL queries in app.py to match your specific data or analysis needs. Visualizations: Customize the Plotly visualizations by editing the Dash components in the layout section. UI/Styling: Use Bootstrap components to change the layout and look of the dashboard. That's it! You should now be able to run and interact with the User Spending Dashboard.
