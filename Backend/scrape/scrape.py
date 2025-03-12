from pydantic import BaseModel,Httpurl
from bs4 import BeautifulSoup
from pyppeteer import launch
import json
import time
import asyncio

urls = [
    'https://en.wikipedia.org/wiki/Formula_One',
    'https://www.skysports.com/f1/news/12433/13322586/f1-2025-season-full-calendar-race-schedule-driver-line-ups-rule-changes-how-to-watch-whats-new',
    'https://www.formula1.com/en/latest/all',
    'https://www.forbes.com/sites/brettknight/2024/12/10/formula-1s-highest-paid-drivers-2024/',
    'https://www.formula1.com/en/latest/article/international-womens-day-trailblazing-women-f1-past-and-present.6rY8yNSHyQ15dyvqgxZDE0',
    'https://www.formula1.com/en/results/2024/races',
    'https://en.wikipedia.org/wiki/2024_Formula_One_World_Championship',
    'https://en.wikipedia.org/wiki/2023_Formula_One_World_Championship',
    'https://en.wikipedia.org/wiki/2022_Formula_One_World_Championship', 
    'https://www.forbes.com/sites/brettknight/2023/11/29/formula-1s-highest-paid-drivers-2023/'   
]

# ✅ Define Pydantic model for scraped F1 data , as this is how we will get to see data in the output
class F1Data(BaseModel):
    url: str
    title:str

async def scrape_f1_website(url: str):
    """Scrapes F1 data from a given URL using Pyppeteer. Pyppeteer ensures we get a fully loaded page, and then BeautifulSoup extracts the important information! """
    browser = await launch()
    page = await browser.newPage()
    await page.goto(urls)
    await page.screenshot({'path': 'example.png'})

    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')

    print(dimensions)
    # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
    await browser.close()
    

async def main():
    """Scrapes F1 data and saves it to a JSON file using Pydantic."""
    all_data = []
    for url in urls:
        print(f"Scrapping {url}")
        #now we first fetch data from our above function and add it to all_data in form of json
        articles = await scrape_f1_website(url)
        #Extend list by appending elements from the iterable.
        all_data.extend()
asyncio.get_event_loop().run_until_complete(scrape_f1_website())