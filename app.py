from flask import Flask, render_template, request
from scrapper import Scraper # Import the extract_reviews function from scraper.py
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reviews', methods=['POST'])
def reviews():
    product_id = request.form['product_id']

    # Create an instance of ReviewScraper
    scraper = Scraper(product_id)

    # Call the extract_reviews method to get the reviews data
    users_data = scraper.extract_reviews()

    return render_template('reviews.html', users_data=users_data)

if __name__ == '__main__':
    app.run(debug=True)