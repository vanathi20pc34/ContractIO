from flask import Flask, request, jsonify, render_template
import openai
import pandas as pd

app = Flask(__name__)

# Load your CSV data
# Load your CSV data
data = pd.read_csv("lease_data_2.csv")

# Convert the date columns with the correct format
data['lease_start_date'] = pd.to_datetime(data['lease_start'], format='%m/%d/%Y', errors='coerce')
data['lease_end_date'] = pd.to_datetime(data['lease_end'], format='%m/%d/%Y', errors='coerce')


# OpenAI API Key (replace with your own key)
openai.api_key = "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"

# Home route with form
@app.route('/')
def home():
    return '''
    <form action="/query" method="post">
        <label for="query">Ask a question:</label><br><br>
        <input type="text" id="query" name="query" placeholder="Type your question"><br><br>
        <button type="submit">Submit</button>
    </form>
    '''

# Query endpoint
@app.route('/query', methods=['POST'])
def query():
    user_query = request.form.get("query")  # Get query from form
    if not user_query:
        return jsonify({"error": "Query is required."}), 400

    # Process question via OpenAI
    try:
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about the lease data."},
            {"role": "user", "content": "How much rent for the month March 2023?"}
        ],
        max_tokens=400
        )
        print(response['choices'][0]['message']['content'])
        answer = response["choices"][0]["text"].strip()
        return f"<h3>Question: {user_query}</h3><p>Answer: {answer}</p><a href='/'>Ask another question</a>"
    except Exception as e:
        return f"<p>Error: {str(e)}</p><a href='/'>Try again</a>"

if __name__ == '__main__':
    app.run(debug=True)
