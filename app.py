from flask import Flask, render_template, request
from scrapper import extract_reviews # Import the extract_reviews function from scraper.py
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    product_id = request.form['product_id']

    users_data = extract_reviews(product_id)

    return render_template('reviews.html', users_data=users_data)

if __name__ == '__main__':
    app.run(debug=True)