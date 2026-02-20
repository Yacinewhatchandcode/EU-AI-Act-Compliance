"""
PRIME.AI Enhanced Prospect Finder v2
Uses multiple strategies to find real prospects with emails.
Strategy 1: Search business directories (Pages Jaunes, Societe.com, etc.)
Strategy 2: Use DuckDuckGo (less bot detection than Google)
Strategy 3: Generate targeted prospect lists by industry
"""
import csv
import os
import sys
import re
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime


# ============================================================
# TARGET SEARCH QUERIES BY INDUSTRY
# ============================================================
INDUSTRIES = {
    "immobilier": {
        "label": "🏠 Immobilier",
        "queries": [
            "site:pagesjaunes.fr agence immobiliere",
            "agence immobilière contact email site:societe.com",
            "\"agence immobilière\" \"@\" email france",
            "immobilier contact@ OR info@ france -site:leboncoin.fr",
        ]
    },
    "beaute": {
        "label": "💄 Beauté & Cosmétiques",
        "queries": [
            "institut beauté contact@ email france",
            "\"salon esthétique\" \"@\" email",
            "cosmétique marque française contact email",
            "site:instagram.com salon beauté france email",
        ]
    },
    "hotels": {
        "label": "🏨 Hôtels & Locations",
        "queries": [
            "hotel boutique france contact@ email",
            "gite chambre hote france email contact",
            "\"location saisonnière\" contact email france",
            "conciergerie airbnb france email contact",
        ]
    },
    "restaurants": {
        "label": "🍽️ Restaurants",
        "queries": [
            "restaurant gastronomique france contact email",
            "traiteur evenementiel france email",
            "\"food truck\" france contact email",
            "brasserie restaurant email contact@",
        ]
    },
    "ecommerce": {
        "label": "🛒 E-commerce",
        "queries": [
            "boutique en ligne france contact email",
            "\"e-commerce\" made in france email contact",
            "artisan createur france email",
            "marque mode française email contact",
        ]
    },
    "coaching": {
        "label": "💼 Coaches & Consultants",
        "queries": [
            "coach business entrepreneur france email",
            "consultant marketing france contact email",
            "formateur professionnel france email",
            "coach sportif personal trainer france email",
        ]
    },
}


def extract_emails_from_text(text):
    """Extract email addresses from text, filtering junk."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)
    
    blacklist = [
        'example.com', 'test.com', 'email.com', 'domain.com',
        'sentry.io', 'schema.org', 'w3.org', 'googleapis.com',
        'google.com', 'gstatic.com', 'youtube.com', 'facebook.com',
        'twitter.com', 'instagram.com', 'microsoft.com', 'apple.com',
        'amazon.com', 'github.com', 'cloudflare.com', 'jquery.com',
        'primeai@gmail.com', 'info.primeai@gmail.com',
        'noreply', 'no-reply', 'unsubscribe', 'mailer-daemon',
        'postmaster', 'webmaster', 'abuse@',
    ]
    
    valid = []
    for e in emails:
        e_lower = e.lower()
        if not any(b in e_lower for b in blacklist):
            if len(e) > 6 and len(e) < 50:  # reasonable length
                valid.append(e_lower)
    
    return list(set(valid))


def search_duckduckgo(query, max_results=20):
    """Search DuckDuckGo (less aggressive bot detection than Google)."""
    try:
        encoded = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'fr-FR,fr;q=0.9',
        })
        
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Extract emails from the search results
            emails = extract_emails_from_text(html)
            
            # Also extract URLs for further scraping
            urls = re.findall(r'href="(https?://[^"]+)"', html)
            
            return emails, urls[:max_results]
    except Exception as e:
        return [], []


def scrape_page_for_emails(url):
    """Visit a URL and extract email addresses from it."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html',
        })
        
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8', errors='ignore')
            return extract_emails_from_text(html)
    except:
        return []


def find_prospects(industries=None, scrape_depth=3):
    """
    Full prospect finding pipeline.
    1. Search DuckDuckGo for each industry 
    2. Visit top result pages to scrape emails
    3. Save everything to CSV
    """
    
    if not industries:
        industries = list(INDUSTRIES.keys())
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_csv = os.path.join(os.path.dirname(__file__), f"prospects_{timestamp}.csv")
    
    all_prospects = []
    seen_emails = set()
    
    print(f"\n{'='*60}")
    print(f"  🚀 PRIME.AI Prospect Finder v2")
    print(f"  Industries: {len(industries)}")
    print(f"  Strategy: DuckDuckGo + Page Scraping")
    print(f"{'='*60}")
    
    for industry_key in industries:
        industry = INDUSTRIES.get(industry_key)
        if not industry:
            print(f"\n  ⚠️ Unknown industry: {industry_key}")
            continue
        
        print(f"\n{industry['label']}")
        print(f"  {len(industry['queries'])} queries")
        
        for query in industry['queries']:
            print(f"  🔍 {query[:55]}...")
            
            # Step 1: Search DuckDuckGo
            emails, urls = search_duckduckgo(query)
            
            for email in emails:
                if email not in seen_emails:
                    seen_emails.add(email)
                    domain = email.split('@')[1].split('.')[0]
                    local = email.split('@')[0]
                    prospect = {
                        "name": local.replace('.', ' ').replace('_', ' ').replace('-', ' ').title(),
                        "company": domain.replace('-', ' ').title(),
                        "email": email,
                        "industry": industry_key,
                        "city": "",
                        "source": "duckduckgo",
                        "found_date": datetime.now().strftime("%Y-%m-%d"),
                    }
                    all_prospects.append(prospect)
                    print(f"     ✅ {email}")
            
            # Step 2: Scrape top pages for more emails
            scraped = 0
            for page_url in urls[:scrape_depth]:
                # Skip search engines and social media
                skip = ['duckduckgo.com', 'google.com', 'bing.com', 'facebook.com', 
                        'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com']
                if any(s in page_url for s in skip):
                    continue
                
                page_emails = scrape_page_for_emails(page_url)
                for email in page_emails:
                    if email not in seen_emails:
                        seen_emails.add(email)
                        domain = email.split('@')[1].split('.')[0]
                        local = email.split('@')[0]
                        prospect = {
                            "name": local.replace('.', ' ').replace('_', ' ').replace('-', ' ').title(),
                            "company": domain.replace('-', ' ').title(),
                            "email": email,
                            "industry": industry_key,
                            "city": "",
                            "source": page_url[:80],
                            "found_date": datetime.now().strftime("%Y-%m-%d"),
                        }
                        all_prospects.append(prospect)
                        print(f"     ✅ {email} (from {domain})")
                
                scraped += 1
            
            time.sleep(3)  # Respect rate limits
    
    # Save to CSV
    if all_prospects:
        fieldnames = ["name", "company", "email", "industry", "city", "source", "found_date"]
        with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(all_prospects)
        
        print(f"\n{'='*60}")
        print(f"  ✅ Prospect Search Complete!")
        print(f"  📊 Total unique prospects: {len(all_prospects)}")
        print(f"  📄 CSV saved: {output_csv}")
        print(f"{'='*60}\n")
    else:
        # Create file with headers even if empty
        fieldnames = ["name", "company", "email", "industry", "city", "source", "found_date"]
        with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
        
        print(f"\n{'='*60}")
        print(f"  ⚠️ No prospects found via automated search.")
        print(f"  💡 Try adding prospects manually to: {output_csv}")
        print(f"  💡 Or use Perplexity deep search for better results.")
        print(f"{'='*60}\n")
    
    return output_csv, all_prospects


# ============================================================
# CLI
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("PRIME.AI Prospect Finder v2")
        print("=" * 40)
        print()
        print("Usage:")
        print("  python prospect_finder_v2.py search                 Search ALL industries")
        print("  python prospect_finder_v2.py search immobilier      Search specific industry")
        print("  python prospect_finder_v2.py search beaute hotels   Search multiple")
        print()
        print("Available industries:")
        for key, val in INDUSTRIES.items():
            print(f"  {key:20s} {val['label']}")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "search":
        ind = sys.argv[2:] if len(sys.argv) > 2 else None
        find_prospects(ind)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
