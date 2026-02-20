"""
PRIME.AI Prospect Finder v4 - FINAL VERSION
Uses the French Government Open API (data.gouv.fr) to find real businesses.
Then finds their websites and emails via web scraping.
Supports ALL industries relevant to visual content.
"""
import csv
import os
import sys
import re
import json
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin, urlparse


# ============================================================
# INDUSTRY SEARCH TERMS (NAF/APE codes + keywords)
# ============================================================
INDUSTRIES = {
    "immobilier": {
        "label": "🏠 Immobilier",
        "queries": [
            "agence immobiliere",
            "transaction immobiliere",
            "gestion immobiliere paris",
            "mandataire immobilier",
        ],
    },
    "beaute": {
        "label": "💄 Beauté & Cosmétiques",
        "queries": [
            "institut de beaute",
            "salon esthetique",
            "cosmetique",
            "salon de coiffure",
            "spa bien etre",
        ],
    },
    "hotels": {
        "label": "🏨 Hôtels & Hébergement",
        "queries": [
            "hotel",
            "chambre hotes",
            "gite location saisonniere",
            "conciergerie location",
        ],
    },
    "restaurants": {
        "label": "🍽️ Restaurants & Traiteurs",
        "queries": [
            "restaurant",
            "traiteur evenementiel",
            "boulangerie patisserie",
            "brasserie",
        ],
    },
    "ecommerce": {
        "label": "🛒 Commerce & Boutiques",
        "queries": [
            "boutique mode",
            "commerce en ligne",
            "bijouterie artisanale",
            "maroquinerie",
        ],
    },
    "coaching": {
        "label": "💼 Coaches & Indépendants",
        "queries": [
            "coach professionnel",
            "consultant marketing",
            "formation professionnelle",
            "architecte interieur",
            "photographe professionnel",
        ],
    },
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.9',
}


def search_french_businesses(query, page=1, per_page=25):
    """Search French government business registry API."""
    url = f"https://recherche-entreprises.api.gouv.fr/search?q={quote_plus(query)}&page={page}&per_page={per_page}"
    
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            businesses = []
            
            for result in data.get("results", []):
                name = result.get("nom_complet", "")
                siren = result.get("siren", "")
                siege = result.get("siege", {})
                
                biz = {
                    "name": name.title() if name else "",
                    "siren": siren,
                    "address": siege.get("adresse", ""),
                    "city": siege.get("libelle_commune", ""),
                    "postal_code": siege.get("code_postal", ""),
                    "activity": siege.get("activite_principale", ""),
                }
                
                if biz["name"] and biz["city"]:
                    businesses.append(biz)
            
            total = data.get("total_results", 0)
            return businesses, total
        else:
            return [], 0
    except Exception as e:
        print(f"    ⚠️ API error: {e}")
        return [], 0


def find_website_and_email(business_name, city):
    """
    Try to find website and email for a business.
    Uses DuckDuckGo Instant Answer API (doesn't get blocked).
    """
    try:
        query = f"{business_name} {city}"
        url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_redirect=1"
        resp = requests.get(url, headers=HEADERS, timeout=8)
        
        if resp.status_code == 200:
            data = resp.json()
            
            # Check for official website
            website = data.get("AbstractURL", "") or data.get("Results", [{}])[0].get("FirstURL", "") if data.get("Results") else ""
            
            # Try to find emails in the abstract
            abstract = data.get("Abstract", "") + data.get("AbstractText", "")
            emails = extract_emails(abstract)
            
            return website, emails
    except:
        pass
    
    return "", []


def extract_emails(text):
    """Extract email addresses from text."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    raw = re.findall(pattern, text)
    
    blacklist = ['example.com', 'test.com', 'google.com', 'facebook.com',
                 'twitter.com', 'wordpress.com', 'wix.com', 'noreply',
                 'no-reply', 'unsubscribe', 'primeai']
    
    return [e.lower() for e in raw if not any(b in e.lower() for b in blacklist) 
            and len(e) > 6 and len(e) < 60]


def scrape_website_for_email(url):
    """Visit a website and extract email addresses."""
    emails = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True)
        if resp.status_code == 200:
            emails.extend(extract_emails(resp.text))
            
            # Parse the page for contact links and mailto:
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Mailto links
            for link in soup.find_all('a', href=True):
                if 'mailto:' in link['href']:
                    email = link['href'].replace('mailto:', '').split('?')[0].strip()
                    if '@' in email:
                        emails.append(email.lower())
            
            # Try /contact page
            for link in soup.find_all('a', href=True):
                href = link['href'].lower()
                text = (link.get_text() or '').lower()
                if 'contact' in href or 'contact' in text:
                    contact_url = link['href']
                    if contact_url.startswith('/'):
                        contact_url = urljoin(url, contact_url)
                    if contact_url.startswith('http') and contact_url != url:
                        try:
                            r2 = requests.get(contact_url, headers=HEADERS, timeout=8)
                            if r2.status_code == 200:
                                emails.extend(extract_emails(r2.text))
                                soup2 = BeautifulSoup(r2.text, 'html.parser')
                                for ml in soup2.find_all('a', href=True):
                                    if 'mailto:' in ml['href']:
                                        e = ml['href'].replace('mailto:', '').split('?')[0].strip()
                                        if '@' in e:
                                            emails.append(e.lower())
                        except:
                            pass
                    break
    except:
        pass
    
    return list(set(emails))


def find_prospects(industries_filter=None, max_per_industry=50, scrape_websites=True):
    """
    Main prospect finding pipeline.
    1. Search French business registry API
    2. Try to find emails for each business
    """
    
    industries_to_search = industries_filter or list(INDUSTRIES.keys())
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"prospects_{timestamp}.csv")
    
    all_prospects = []
    seen = set()
    
    print(f"\n{'='*60}")
    print(f"  🚀 PRIME.AI Prospect Finder v4")
    print(f"  Source: French Government Business Registry")
    print(f"  Industries: {len(industries_to_search)}")
    print(f"  Max per industry: {max_per_industry}")
    print(f"  Website scraping: {'ON' if scrape_websites else 'OFF'}")
    print(f"{'='*60}")
    
    for ind_key in industries_to_search:
        ind = INDUSTRIES.get(ind_key)
        if not ind:
            continue
        
        print(f"\n{ind['label']}")
        industry_count = 0
        
        for query in ind['queries']:
            if industry_count >= max_per_industry:
                break
            
            print(f"  🔍 {query}...")
            
            # Calculate how many per page
            remaining = max_per_industry - industry_count
            per_page = min(remaining, 25)
            
            businesses, total = search_french_businesses(query, per_page=per_page)
            print(f"     📊 {total} businesses found, processing {len(businesses)}")
            
            for biz in businesses:
                key = biz['siren']
                if key in seen:
                    continue
                seen.add(key)
                
                prospect = {
                    "name": biz['name'],
                    "company": biz['name'],
                    "email": "",
                    "phone": "",
                    "address": biz['address'],
                    "city": biz['city'],
                    "postal_code": biz['postal_code'],
                    "industry": ind_key,
                    "siren": biz['siren'],
                    "website": "",
                    "found_date": datetime.now().strftime("%Y-%m-%d"),
                }
                
                all_prospects.append(prospect)
                industry_count += 1
                print(f"     ✅ {biz['name'][:40]} | {biz['city']}")
            
            time.sleep(1)  # Respect API rate limits
    
    # Save to CSV
    if all_prospects:
        fieldnames = list(all_prospects[0].keys())
        with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for p in all_prospects:
                writer.writerow(p)
    
    print(f"\n{'='*60}")
    print(f"  ✅ Prospect Search Complete!")
    print(f"  📊 Total businesses found: {len(all_prospects)}")
    print(f"  📄 CSV: {output_csv}")
    print(f"")
    print(f"  💡 Next steps:")
    print(f"     1. Open the CSV in Excel")
    print(f"     2. Search businesses on Google/Facebook to find emails")
    print(f"     3. Or use: python prospect_finder_v4.py enrich {output_csv}")
    print(f"{'='*60}\n")
    
    return output_csv, all_prospects


def enrich_prospects(csv_path, max_scrape=20):
    """Enrich a prospect CSV by scraping business websites for emails."""
    
    prospects = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        prospects = list(reader)
    
    print(f"\n{'='*60}")
    print(f"  🔧 Enriching {len(prospects)} prospects with emails")
    print(f"  Max scraping: {max_scrape} websites")
    print(f"{'='*60}\n")
    
    enriched = 0
    for i, p in enumerate(prospects):
        if enriched >= max_scrape:
            break
        if p.get('email'):
            continue
        
        name = p.get('name', p.get('company', ''))
        city = p.get('city', '')
        
        print(f"  [{i+1}/{len(prospects)}] {name[:40]} ({city})...", end=" ")
        
        # Try DuckDuckGo instant answer
        website, emails = find_website_and_email(name, city)
        
        if website and not emails and website.startswith('http'):
            # Scrape the website
            emails = scrape_website_for_email(website)
            p['website'] = website
        
        if emails:
            p['email'] = emails[0]
            enriched += 1
            print(f"✅ {emails[0]}")
        else:
            print(f"❌ no email found")
        
        time.sleep(2)
    
    # Save updated CSV
    enriched_csv = csv_path.replace('.csv', '_enriched.csv')
    if prospects:
        fieldnames = list(prospects[0].keys())
        with open(enriched_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for p in prospects:
                writer.writerow(p)
    
    print(f"\n  📧 Emails found: {enriched}")
    print(f"  📄 Saved: {enriched_csv}")
    
    return enriched_csv


# ============================================================
# CLI
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("PRIME.AI Prospect Finder v4")
        print("=" * 45)
        print("  Source: French Government Business Registry")
        print()
        print("Usage:")
        print("  python prospect_finder_v4.py search                   All industries")
        print("  python prospect_finder_v4.py search immobilier        One industry")
        print("  python prospect_finder_v4.py search beaute hotels     Multiple")
        print("  python prospect_finder_v4.py enrich prospects.csv     Find emails")
        print()
        print("Industries:")
        for k, v in INDUSTRIES.items():
            print(f"  {k:20s} {v['label']}")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "search":
        ind = sys.argv[2:] if len(sys.argv) > 2 else None
        find_prospects(ind)
    
    elif cmd == "enrich":
        if len(sys.argv) < 3:
            print("Error: specify CSV path")
            sys.exit(1)
        enrich_prospects(sys.argv[2])
    
    else:
        print(f"Unknown: {cmd}")
