import json
import csv
from scrapper import extract_reviews

def save(key):
    wynik = extract_reviews(key)
    with open('test.json', 'w') as f:
        json.dump(wynik, f, indent=4)

    with open('test.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=[
            "id", "name", "recommended", "rating", "is_bought",
            "time_added", "time_bought", "liked", "dissliked",
            "opinion", "features", "flaws"
        ])
        writer.writeheader()
        writer.writerows(wynik)
