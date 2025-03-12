from pydantic import BaseModel, HttpUrl
from typing import List,Optional
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
    url: HttpUrl
    title:str
    content:str

async def scrape_f1_website(url: str) -> List[F1Data]: # A list containing elements of type F1Data , The function returns a list of F1Article objects.
    """Scrapes F1 data from a given URL using Pyppeteer. Pyppeteer ensures we get a fully loaded page, and then BeautifulSoup extracts the important information! """
    browser = await launch()
    page = await browser.newPage() #Make new page on this browser and return its object.
    await page.goto(url, {"waitUntil": "domcontentloaded"})
    await page.waitForSelector("body") 
    
    html = await page.evaluate("document.documentElement.innerHTML")  # ✅ Correct
    await browser.close()
    
    #after this BeautifulSoup will function
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    
    articles = soup.find_all("article")
    sections = soup.find_all(["h1", "h2", "h3", "p", "div"])  # Find all relevant tags
    
    data = []
    
    for article in articles:
        title = article.find("h2") or article.find("h3") or article.find("h4")
        content = article.find("p") or article.find("div")

        if title and content:
            try:
                # ✅ Validate data using Pydantic
                article_data = F1Data(
                    url=url,
                    title=title.get_text().strip(),
                    content=content.get_text(separator="\n").strip()
                )
                data.append(article_data)
            except Exception as e:
                print(f"Skipping invalid data: {e}")
    
    
    for section in sections:
        # Extract titles (h1, h2, h3)
        if section.name in ["h1", "h2", "h3"]:
            title = section.get_text().strip()
            next_sibling = section.find_next_sibling(["p", "div"])  # Look for the next paragraph or div
            
            content = "No content available"  # ✅ Default value to prevent errors
            
            if next_sibling:
                content = next_sibling.get_text(separator="\n").strip()
            
            try:
                # ✅ Validate using Pydantic
                section_data = F1Data(
                    url=url,
                    title=title,
                    content=content
                )
                data.append(section_data)
            except Exception as e:
                print(f"Skipping invalid data: {e}")
   
    return data
    
async def main():
    """Scrapes F1 data and saves it to a JSON file using Pydantic."""
    all_data = []
    for url in urls:
        print(f"Scrapping {url}")
        #now we first fetch data from our above function and add it to all_data in form of json
        articles = await scrape_f1_website(url)
        #Extend list by appending elements from the iterable.
        #Converts a Pydantic model to a Python dictionary. article.dict()
        #Converts all F1Article objects into dictionaries. [article.dict() for article in articles]
        #Adds those dictionaries into all_data for further use (e.g., saving to JSON). all_data.extend([])
        #This prevents the TypeError and ensures JSON can be saved correctly.
        all_data.extend([article.model_dump(mode="json") for article in articles])
    
    #now we need to open one JSON file that will keep the HTML
    #Open the file for writing. Truncates the file if it already exists. Creates a new file if it does not exist.
    with open("scraped_f1_data.json", "w") as file:
        json.dump(all_data, file, indent=4)  
        
    print("Scraping completed. Data saved.")


if __name__ == "__main__":
    asyncio.run(main())