import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://g1.globo.com/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

posts = soup.find_all("div", class_="feed-post-body")

data = []

for post in posts:
    link_tag = post.find("a")
    if link_tag:
        title = link_tag.text.strip()
        link = link_tag['href']
        
        try:
            article_resp = requests.get(link, headers=headers)
            article_soup = BeautifulSoup(article_resp.text, 'html.parser')
            subtitle_tag = article_soup.find("h2", class_="content-head__subtitle")
            subtitle = subtitle_tag.text.strip() if subtitle_tag else ""
        except Exception as e:
            subtitle = ""
        
        data.append({
            "Title": title,
            "Link": link,
            "Subtitle": subtitle
        })

df = pd.DataFrame(data)
df.to_excel("noticias_g1.xlsx", index=False)

print("✅ Arquivo 'noticias_g1.xlsx' salvo com sucesso.")
