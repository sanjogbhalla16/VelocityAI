## **F1 Web Scraper Readme**

This repository contains a **Formula 1 Web Scraper** that extracts F1-related data from multiple sources, including **Wikipedia, Formula1.com, SkySports, and Forbes**. The scraper loads web pages using **Pyppeteer** (a headless browser) and extracts relevant content such as **headlines, articles, and statistics**. The extracted data is then saved in **JSON format**.

---

## **🔹 Features**

- 🏎️ **Scrapes Formula 1-related websites** for news, stats, and updates.
- 🌍 **Supports dynamic JavaScript-rendered pages** using Pyppeteer.
- 📄 **Extracts meaningful content** (titles, paragraphs, and key sections).
- 💾 **Saves scraped data in a structured JSON format**.
- ✅ **Uses Pydantic for validation** to ensure clean and consistent data.

---

## **🔹 Setup Instructions**

This scraper requires **Python 3.7+** and the following dependencies:

### **1️⃣ Install Google Chrome & Chromium Driver**

The scraper uses a headless Chrome browser. Install Chrome and its driver:

```sh
sudo apt-get install google-chrome
sudo apt install chromium-chromedriver
```

### **2️⃣ Clone the Repository**

```sh
git clone https://github.com/your-repo/f1-chatbot.git
cd f1-chatbot/scraper
```

### **3️⃣ Install Python Dependencies**

```sh
pip3 install -r requirements.txt
```

---

## **🔹 Configuration**

- You can modify the list of **URLs to scrape** inside `scraper.py` under the `urls` list.
- The **output file** (default: `scraper/scraped_f1_data.json`) can be changed in the `main()` function.

---

## **🔹 How to Run the Scraper**

To start the scraper, run:

```sh
python3 scraper.py
```

---

## **🔹 How the Scraper Works**

1. **Loads Web Pages with Pyppeteer**

   - Uses **Pyppeteer** (headless browser) to load **JavaScript-rendered** content.
   - Extracts **fully loaded HTML** using `document.documentElement.innerHTML`.

2. **Parses Content with BeautifulSoup**

   - Filters out **articles, headlines, paragraphs, and key sections**.

3. **Validates and Saves Data**
   - Uses **Pydantic** to ensure valid data before saving.
   - Stores the scraped F1 data in **JSON format**.

---

## **🔹 Output Format**

The scraped data is saved in `scraper/scraped_f1_data.json` in the following format:

```json
[
  {
    "url": "https://en.wikipedia.org/wiki/Formula_One",
    "title": "Formula One",
    "content": "Formula One, commonly abbreviated as F1, is the highest class of international racing..."
  },
  {
    "url": "https://www.formula1.com/en/results/2024/races",
    "title": "F1 2024 Race Results",
    "content": "Complete race results for the 2024 Formula 1 season..."
  }
]
```

---

## **🔹 Notes**

- This scraper is designed for **F1-related websites**.
- It may **not work properly on sites with heavily protected content**.
- For best results, ensure **Google Chrome is installed and up to date**.

---

## **🔹 Future Improvements**

✅ **Enhance Content Filtering** – Improve extraction of structured F1 stats.  
✅ **Scrape More F1 Websites** – Add sources like ESPN, BBC Sport, and Autosport.  
✅ **Improve Speed** – Optimize Pyppeteer for faster scraping.

---

🚀 **Enjoy your AI-powered F1 chatbot!**
