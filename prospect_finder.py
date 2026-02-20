"""
Prospect Finder for PRIME.AI
Deep searches the web for businesses that need AI-generated visual content.
Targets: real estate, beauty, hotels, restaurants, e-commerce, coaches, etc.
"""
import csv
import os
import sys
import re
import subprocess
import time
from datetime import datetime


# ============================================================
# TARGET INDUSTRIES (highest demand for visual content)
# ============================================================
SEARCH_QUERIES = {
    "real_estate": [
        "agence immobilière email contact France",
        "agences immobilières paris contact email",
        "agent immobilier lyon bordeaux marseille email",
        "réseau immobilier franchise France contact",
    ],
    "beauty_cosmetics": [
        "marque cosmétique française email contact",
        "salon beauté esthétique France email",
        "institut beauté paris lyon email contact",
        "marque bio skincare France email",
    ],
    "hotels_vacation": [
        "hôtel boutique France email contact",
        "location vacances gîte France email",
        "chambre hôte France email contact",
        "Airbnb management France email contact",
    ],
    "restaurants_food": [
        "restaurant gastronomique France email contact",
        "traiteur événementiel France email",
        "food truck France email contact",
        "restaurant paris lyon marseille email",
    ],
    "ecommerce": [
        "boutique en ligne France email contact",
        "e-commerce mode française email",
        "artisan créateur boutique email France",
        "marque Made in France email contact",
    ],
    "coaches_consultants": [
        "coach business France email contact",
        "consultant marketing digital France email",
        "formateur entrepreneur France email",
        "coach sportif personal trainer France email",
    ],
}


def extract_emails(text):
    """Extract email addresses from text."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)
    # Filter junk
    blacklist = ['example.com', 'test.com', 'email.com', 'domain.com', 
                 'sentry.io', 'schema.org', 'w3.org', 'googleapis.com',
                 'primeai@gmail.com', 'info.primeai@gmail.com']
    return [e.lower() for e in emails if not any(b in e.lower() for b in blacklist)]


def search_google_for_prospects(query, num_results=10):
    """Use Google search to find prospect emails."""
    try:
        import urllib.request
        import urllib.parse
        
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}&num={num_results}"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            return extract_emails(html)
    except Exception as e:
        print(f"    Search failed: {e}")
        return []


def search_with_browser(query):
    """Use browser_tools.py to search Google and screenshot results."""
    try:
        result = subprocess.run(
            ['python', os.path.join(os.path.dirname(__file__), 'browser_tools.py'), 
             'google', query],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout
    except:
        return ""


def find_prospects(industries=None, output_csv=None):
    """Search for prospects across specified industries."""
    
    if not output_csv:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_csv = os.path.join(os.path.dirname(__file__), f"prospects_{timestamp}.csv")
    
    if not industries:
        industries = list(SEARCH_QUERIES.keys())
    
    all_prospects = []
    seen_emails = set()
    
    print(f"\n{'='*60}")
    print(f"  PRIME.AI Prospect Finder")
    print(f"  Industries: {', '.join(industries)}")
    print(f"{'='*60}\n")
    
    for industry in industries:
        queries = SEARCH_QUERIES.get(industry, [])
        print(f"\n📂 {industry.upper().replace('_', ' ')}")
        print(f"   {len(queries)} search queries")
        
        for query in queries:
            print(f"   🔍 Searching: {query[:60]}...")
            emails = search_google_for_prospects(query)
            
            for email in emails:
                if email not in seen_emails:
                    seen_emails.add(email)
                    # Try to extract name/company from email
                    local = email.split('@')[0]
                    domain = email.split('@')[1].split('.')[0]
                    
                    prospect = {
                        "name": local.replace('.', ' ').replace('_', ' ').replace('-', ' ').title(),
                        "company": domain.title(),
                        "email": email,
                        "industry": industry,
                        "city": "",
                        "source": query[:50],
                        "found_date": datetime.now().strftime("%Y-%m-%d"),
                    }
                    all_prospects.append(prospect)
                    print(f"      ✅ Found: {email}")
            
            time.sleep(2)  # Be polite to Google
    
    # Save to CSV
    if all_prospects:
        with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=all_prospects[0].keys(), delimiter=";")
            writer.writeheader()
            writer.writerows(all_prospects)
    
    print(f"\n{'='*60}")
    print(f"  Prospect Search Complete!")
    print(f"  📊 Total prospects found: {len(all_prospects)}")
    print(f"  📄 Saved to: {output_csv}")
    print(f"{'='*60}\n")
    
    return output_csv, all_prospects


def create_sample_csv():
    """Create a sample prospect CSV for testing."""
    sample_path = os.path.join(os.path.dirname(__file__), "prospects_sample.csv")
    
    sample_data = [
        {"name": "Jean Dupont", "company": "ImmoPlus Paris", "email": "contact@immoplus.fr", 
         "industry": "real_estate", "city": "Paris"},
        {"name": "Marie Martin", "company": "Beauté Bio", "email": "info@beautebio.fr",
         "industry": "beauty_cosmetics", "city": "Lyon"},
        {"name": "Pierre Bernard", "company": "Hôtel Le Charme", "email": "reserv@lecharme.fr",
         "industry": "hotels_vacation", "city": "Nice"},
        {"name": "Sophie Leroy", "company": "La Table d'Or", "email": "contact@latabledoor.fr",
         "industry": "restaurants_food", "city": "Bordeaux"},
        {"name": "Thomas Petit", "company": "Mode Éthique", "email": "hello@modeethique.fr",
         "industry": "ecommerce", "city": "Marseille"},
    ]
    
    with open(sample_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=sample_data[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(sample_data)
    
    print(f"Sample CSV created: {sample_path}")
    return sample_path


# ============================================================
# CLI INTERFACE
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("PRIME.AI Prospect Finder")
        print("=" * 40)
        print()
        print("Usage:")
        print("  python prospect_finder.py search              Search ALL industries")
        print("  python prospect_finder.py search real_estate  Search specific industry")
        print("  python prospect_finder.py sample              Create sample CSV")
        print()
        print("Industries:")
        for key in SEARCH_QUERIES:
            print(f"  - {key}")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "search":
        industries = sys.argv[2:] if len(sys.argv) > 2 else None
        find_prospects(industries)
    
    elif cmd == "sample":
        create_sample_csv()
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
