import requests
from bs4 import BeautifulSoup

klucz = "32693267;02517"
strona = f"https://www.ceneo.pl/{klucz}#tab=reviews"

req = requests.get(strona)

soup = BeautifulSoup(req.content, "html.parser")
users_data = []

user_posts = soup.find_all("div", class_="user-post")

for post in user_posts:
    user_id = post.get("data-entry-id", "N/A")
    user_name = post.find("span", class_="user-post__author-name").get_text().strip()
    user_recommendation_elem = post.find("span", class_="user-post__author-recomendation")
    user_recommendation = user_recommendation_elem.find("em", class_="recommended").get_text().strip() if user_recommendation_elem else "N/A"
    user_rating_elem = post.find("span", class_="user-post__score-count")
    user_rating = user_rating_elem.get_text().strip() if user_rating_elem else "N/A"    
    is_bought = post.find("span", class_="user-post__published")
    user_is_bought = "użytkowania" in is_bought.get_text().strip() if is_bought else False
    user_time_elem = post.find("time")
    user_time = user_time_elem["datetime"] if user_time_elem else "N/A"
    user_when_bought_elem = post.find("span", class_="user-post__published")
    user_when_bought = user_when_bought_elem.get_text(strip=True).split(",")[0] if user_when_bought_elem else "N/A"
    user_liked = post.select_one(".vote-yes span").get_text(strip=True) if post.select_one(".vote-yes span") else "0"
    user_dissliked = post.select_one(".vote-no span").get_text(strip=True) if post.select_one(".vote-no span") else "0"
    user_opinion = post.find("div", class_="user-post__text").get_text().strip()

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

for user in users_data:
    print(user)
