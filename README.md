# pp2-ceneo-scraper
A Python and Flask-based web application to scrape product data from Ceneo.pl and visualize it.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Libraries Used](#libraries-used)
- [Contributing](#contributing)

## Description

This project scrapes product data from Ceneo.pl using Python's `requests` and `BeautifulSoup` libraries. The data is processed and can be exported in JSON and CSV formats. Additionally, it provides data visualization using `matplotlib`.

## Features

- Scrape product data from Ceneo.pl
- Export data in JSON and CSV formats
- Visualize data using matplotlib
- Flask-based web interface for interaction

## Installation

### Prerequisites

- Python 3.x
- Flask

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/MichBurl/pp2-ceneo-scraper.git
    cd pp2-ceneo-scraper
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```python app.py
    ```

## Usage

1. Open your browser and navigate to `http://127.0.0.1:5000`.
2. Enter the Ceneo product URL or other required inputs.
3. Click the "Scrape" button to start scraping.
4. View the scraped data, export it, or visualize it using the provided options.

## Libraries Used

- **requests**: For making HTTP requests to Ceneo.pl.
- **BeautifulSoup**: For parsing and navigating the HTML content.
- **json**: For exporting data in JSON format.
- **csv**: For exporting data in CSV format.
- **matplotlib.pyplot**: For data visualization.
- **base64**: For encoding images for display.
- **BytesIO**: For handling binary data.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.
