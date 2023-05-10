from parsel import Selector
import requests
import time
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        return response.text
    except (requests.ReadTimeout, requests.HTTPError):
        return None
    finally:
        time.sleep(1)


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(html_content)
    return selector.css("a.cs-overlay-link::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    return selector.css("a.next::attr(href)").get()


# Requisito 4
def scrape_news(html_content):
    selector = Selector(html_content)
    return {
        "url": selector.css("link[rel='canonical']::attr(href)").get(),
        "title": selector.css("h1.entry-title::text").get().strip(),
        "timestamp": selector.css("li.meta-date::text").get(),
        "writer": selector.css("span > a.url::text").get(),
        "reading_time": int(
            selector.css("li.meta-reading-time::text").get().split()[0]
        ),
        "summary": "".join(
            selector.css(".entry-content > p:first-of-type *::text").getall()
        ).strip(),
        "category": selector.css("a.category-style > span.label::text").get(),
    }


# Requisito 5
def get_tech_news(amount):
    BASE_URL = "https://blog.betrybe.com/"
    html_content = fetch(BASE_URL)
    news_urls = scrape_updates(html_content)
    all_news = []
    for index in range(amount):
        try:
            all_news.append(scrape_news(fetch(news_urls[index])))
        except IndexError:
            html_content = fetch(scrape_next_page_link(html_content))
            news_urls.extend(scrape_updates(html_content))
            all_news.append(scrape_news(fetch(news_urls[index])))
    create_news(all_news)
    return all_news
