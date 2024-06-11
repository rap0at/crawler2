from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

app = Flask(__name__)

# Define the search function
def search_links(keyword, sites):
    one_week_ago = datetime.now() - timedelta(days=7)
    formatted_date = one_week_ago.strftime('%Y-%m-%d')
    links = []

    for site in sites:
        query = f"{keyword} site:{site} after:{formatted_date}"
        url = f"https://www.google.com/search?q={query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        
        for g in soup.find_all('div', class_='BVG0Nb'):
            link = g.find('a')
            if link and 'href' in link.attrs:
                links.append(link['href'])
            if len(links) >= 20:
                break

    return links[:20]  # Limit to 20 links

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == 'POST':
        keyword1 = request.form.get('keyword1')
        keyword2 = request.form.get('keyword2')
        keyword3 = request.form.get('keyword3')
        sites = request.form.get('sites').split(',')

        if keyword1:
            results['Keyword 1'] = search_links(keyword1, sites)
        if keyword2:
            results['Keyword 2'] = search_links(keyword2, sites)
        if keyword3:
            results['Keyword 3'] = search_links(keyword3, sites)

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
