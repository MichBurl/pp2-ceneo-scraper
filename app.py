from flask import Flask, render_template, request, redirect, url_for
from scrapper import Scraper  # Import the Scraper class from scraper.py
import json
import csv
import io

app = Flask(__name__)

# Define a global variable to store the scraped data
global_users_data = []

menu = [
    {"name": "Ekstrakcja opinii", "url": "/extract_reviews"},
    {"name": "Lista produktów", "url": "/product_list"},
    {"name": "Strona główna", "url": "/"},
    {"name": "O autorze", "url": "/about"}
]

# Funkcja renderująca szablon z menu
def render_with_menu(template_name):
    return render_template(template_name, menu=menu)

@app.route('/')
def index():
    return render_with_menu('index.html')

@app.route('/extract_reviews')
def extract_reviews():
    return render_with_menu('extract_reviews.html')

@app.route('/reviews', methods=['POST'])
def reviews():
    product_id = request.form['product_id']

    # Validate product ID
    if not product_id or not product_id.isdigit():
        error_message = "Invalid product ID."
        return redirect(url_for('error', error_message=error_message))

    # Create an instance of Scraper
    scraper = Scraper(product_id)

    try:
        # Call the extract_reviews method to get the reviews data
        global global_users_data
        global_users_data = scraper.extract_reviews()
        return render_template('reviews.html', users_data=global_users_data)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return redirect(url_for('error', error_message=error_message))

# Obsługa błędów
@app.route('/error/<error_message>')
def error(error_message):
    return render_template('error.html', error_message=error_message)

@app.route('/download_csv')
def download_csv():
    global global_users_data
    
    # Prepare CSV data
    csv_data = io.StringIO()
    csv_writer = csv.DictWriter(csv_data, fieldnames=global_users_data[0].keys())
    csv_writer.writeheader()
    csv_writer.writerows(global_users_data)
    
    # Return CSV file as a response
    csv_data.seek(0)  # Move cursor to the beginning of the StringIO object
    return send_file(
        io.BytesIO(csv_data.getvalue().encode('utf-8')),  # Open the StringIO object in binary mode
        mimetype='text/csv',
        download_name='reviews.csv',  # Specify the filename using download_name
        as_attachment=True
    )

@app.route('/download_json')
def download_json():
    global global_users_data
    
    # Prepare JSON data
    json_data = json.dumps(global_users_data, indent=4)
    
    # Return JSON file as a response
    return send_file(
        io.BytesIO(json_data.encode('utf-8')),  # Open the BytesIO object in binary mode
        mimetype='application/json',
        download_name='reviews.json',  # Specify the filename using download_name
        as_attachment=True
    )

@app.route('/product_list')
def product_list():
    return render_with_menu('product_list.html')

@app.route('/about')
def about():
    return render_with_menu('about.html')


if __name__ == '__main__':
    app.run(debug=True)