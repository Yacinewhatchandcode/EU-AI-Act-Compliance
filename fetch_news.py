"""
Fetch latest news from RSS feeds and update the Journal App.
Leverages 'OpenClaw' capabilities by retrieving structured data from external sources.

Usage: python fetch_news.py
"""
import requests
import xml.etree.ElementTree as ET
import json
import os
import time
from datetime import datetime

# Configuration
RSS_FEEDS = [
    "https://artificialintelligenceact.substack.com/feed",  # EU AI Act specific
    # "https://feeds.feedburner.com/TechCrunch/Europe",      # General Tech Europe
]

# Path to the JSON file used by the Next.js app
DATA_DIR = os.path.join("journal_app", "public", "data")
NEWS_FILE = os.path.join(DATA_DIR, "news.json")
SEED_FILE = "NEWS_SEED.json"

def fetch_rss(url):
    print(f"Fetching RSS: {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to fetch {url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_rss(xml_content):
    items = []
    try:
        root = ET.fromstring(xml_content)
        # Handle namespaces if any, but standard RSS strictly has 'channel' -> 'item'
        channel = root.find("channel")
        if channel is None:
            # Maybe Atom?
            pass
            
        for item in channel.findall("item"):
            title = item.find("title").text if item.find("title") is not None else "No Title"
            link = item.find("link").text if item.find("link") is not None else ""
            desc = item.find("description").text if item.find("description") is not None else ""
            pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
            
            # Simple cleaning of HTML in description if present
            # For now, we keep it raw or truncate
            
            items.append({
                "title": title,
                "link": link,
                "summary": desc[:200] + "..." if len(desc) > 200 else desc,
                "date": pub_date,
                "source": "EU AI Act Newsletter",
                "category": "Regulation"
            })
    except Exception as e:
        print(f"Error parsing XML: {e}")
    return items

def main():
    # Ensure data directory exists
    if not os.path.exists(DATA_DIR):
        print(f"Creating directory: {DATA_DIR}")
        os.makedirs(DATA_DIR, exist_ok=True)

    # Load existing news or seed
    current_news = []
    if os.path.exists(NEWS_FILE):
        with open(NEWS_FILE, "r", encoding="utf-8") as f:
            try:
                current_news = json.load(f)
            except:
                pass
    elif os.path.exists(SEED_FILE):
        print("Loading seed data...")
        with open(SEED_FILE, "r", encoding="utf-8") as f:
            current_news = json.load(f)

    # Fetch new items
    new_items = []
    for url in RSS_FEEDS:
        content = fetch_rss(url)
        if content:
            parsed = parse_rss(content)
            new_items.extend(parsed)

    # Deduplicate based on title
    existing_titles = {n.get("title") for n in current_news}
    added_count = 0
    
    for item in new_items:
        if item["title"] not in existing_titles:
            # Add ID
            item["id"] = len(current_news) + added_count + 1
            # Add simplified date if possible
            try:
                # parsed date handling could be better but keeping simple
                pass 
            except:
                pass
            
            # Prepend to list (showing newest first)
            current_news.insert(0, item)
            existing_titles.add(item["title"])
            added_count += 1

    # Save
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(current_news, f, indent=2)

    print(f"Successfully updated news. Added {added_count} new articles.")
    print(f"Total articles: {len(current_news)}")

if __name__ == "__main__":
    main()
