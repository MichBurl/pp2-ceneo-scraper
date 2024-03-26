import requests
from bs4 import BeautifulSoup
import re
import json
import csv

class Scraper:
    def __init__(self, product_id):
        self.product_id = product_id
        self.users_data = []
    
    def extract_reviews(self):
        klucz = self.product_id
        users_data = []

        for i in range(1,1000):
            strona = f"https://www.ceneo.pl/{klucz}/opinie-{i}"

            req = requests.get(strona)
            soup = BeautifulSoup(req.content, "html.parser")
            user_posts = soup.find_all("div", class_="user-post")

            #To stop when reaches an end
            review_count_text = soup.find('div', class_='score-extend__review').get_text()
            # Use regex to extract only the number
            review_count_number = re.search(r'\d+', review_count_text)
            if review_count_number:
                koniec = int(review_count_number.group())
            end = round(koniec/10)+1
            if end < koniec/10+1:
                end+=1
            if i == end:
                break        

            for post in user_posts:
            #ID
                user_id = post.get("data-entry-id", "N/A")
            #NAME
                user_name_element = post.find("span", class_="user-post__author-name") 
                user_name = user_name_element.get_text().strip() if user_name_element else "N/A" 
            #RECOMMENDATION
                user_recommendation_elem = post.find("span", class_="user-post__author-recomendation")
                if user_recommendation_elem:
                    recommended_elem = user_recommendation_elem.find("em", class_="recommended")
                    not_recommended_elem = user_recommendation_elem.find("em", class_="not-recommended")
                    if recommended_elem:
                        user_recommendation = recommended_elem.get_text().strip()
                    elif not_recommended_elem:
                        user_recommendation = not_recommended_elem.get_text().strip()
            #RATING 
                user_rating_elem = post.find("span", class_="user-post__score-count")
                user_rating = user_rating_elem.get_text().strip() if user_rating_elem else "N/A"    
            #IS_BOUGHT
                is_bought = post.find("span", class_="user-post__published")
                user_is_bought = "użytkowania" in is_bought.get_text().strip() if is_bought else False
            #TIME
                user_time_elem = post.find("time")
                user_time = user_time_elem["datetime"] if user_time_elem else "N/A"
            #WHEN_BOUGHT
                user_when_bought_elem = post.find("span", class_="user-post__published")
                user_when_bought = user_when_bought_elem.get_text(strip=True).split(",")[0] if user_when_bought_elem else "N/A"
            #LIKED
                user_liked = post.select_one(".vote-yes span").get_text(strip=True) if post.select_one(".vote-yes span") else "0"
            #DISSLIKED
                user_dissliked = post.select_one(".vote-no span").get_text(strip=True) if post.select_one(".vote-no span") else "0"
            #OPINION
                user_opinion_element = post.find("div", class_="user-post__text")
                user_opinion = post.find("div", class_="user-post__text").text if user_opinion_element else "N/A"
            #FEATURES AND FLAWS
                user_features = []
                user_flaws = []
                review_features = post.find("div", class_="review-feature")
                if review_features:
                    feature_cols = review_features.find_all("div", class_="review-feature__col")
                    for col in feature_cols:
                        title = col.find("div", class_="review-feature__title").get_text(strip=True)
                        items = [item.get_text(strip=True) for item in col.find_all("div", class_="review-feature__item")]
                        if title == "Zalety":
                            user_features.extend(items)
                        elif title == "Wady":
                            user_flaws.extend(items)
                

                
                user_data = {
                    "id": user_id,
                    "name": user_name,
                    "recommended": user_recommendation,
                    "rating": user_rating,
                    "is_bought": user_is_bought,
                    "time_added": user_time,
                    "time_bought": user_when_bought,
                    "liked": user_liked,
                    "dissliked": user_dissliked,
                    "opinion": user_opinion,
                    "features": user_features,
                    "flaws": user_flaws,
                }
                
                users_data.append(user_data)

        return users_data
    
    def save(self):
        wynik = self.extract_reviews()
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