from flask import Flask, request, jsonify, render_template
import pandas as pd
from datetime import datetime
import re 

app = Flask(__name__)
LEASE_DATA_FILE = "lease_data_2.csv"

def load_lease_data():
    try:
        lease_data = pd.read_csv(
            LEASE_DATA_FILE,
            parse_dates=["lease_start", "lease_end"], 
        )
        return lease_data
    except Exception as e:
        raise ValueError(f"Error loading lease data from file: {e}")


def calculate_rent(year, month):
    try:
        
        month_number = datetime.strptime(month, "%B").month
    except ValueError:
        raise ValueError("Invalid month name. Use full month names, e.g., 'March'.")
    
    lease_data = load_lease_data()
    total_rent = 0
    
    
    current_date = pd.Timestamp(f"{year}-{month_number}-01")
    
    for _, lease in lease_data.iterrows():
        start_date = lease["lease_start"]
        end_date = lease["lease_end"]
        
        
        if pd.Timestamp(start_date) <= current_date <= pd.Timestamp(end_date):
            total_rent += lease["rent_monthly"]
    
    return total_rent
@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/query', methods=['POST'])
def handle_query():
    user_input = request.form.get('query') 
    if not user_input:
        return jsonify({"error": "Query is required"}), 400

    try:
        
        match = re.search(r"for the month (\w+) (\d{4})", user_input, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid query format. Use 'How much rent for the month <Month> <Year>?'.")
        
        month = match.group(1).capitalize()
        year = match.group(2)  
        
        total_rent = calculate_rent(int(year), month)
        return render_template('result.html', query=user_input, total_rent=total_rent)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
