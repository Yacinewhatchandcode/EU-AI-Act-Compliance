"""
PRIME.AI Prospect Finder v3
Uses googlesearch-python + BeautifulSoup to properly find business emails.
Scrapes actual business pages (not just search result snippets).
"""
import csv
import os
import sys
import re
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

try:
    from googlesearch import search as gsearch
    HAS_GSEARCH = True
except ImportError:
    HAS_GSEARCH = False
    print("⚠️ googlesearch-python not installed. Run: pip install googlesearch-python")


# ============================================================
# SEARCH QUERIES - Designed to find business CONTACT PAGES
# ============================================================
INDUSTRIES = {
    "immobilier": {
        "label": "🏠 Immobilier",
        "queries": [
            "agence immobilière paris contact",
            "agence immobilière lyon contact email",
            "agence immobilière bordeaux nous contacter",
            "agence immobilière marseille contact",
            "agence immobilière nice contact",
            "agence immobilière nantes contact",
            "agence immobilière toulouse contact email",
            "réseau immobilier indépendant france contact",
        ]
    },
    "beaute": {
        "label": "💄 Beauté & Cosmétiques",
        "queries": [
            "institut de beauté paris contact email",
            "salon esthétique lyon contact",
            "marque cosmétique bio française contact",
            "salon coiffure haut de gamme paris contact",
            "spa bien-être france contact email",
            "maquilleur professionnel paris contact",
        ]
    },
    "hotels": {
        "label": "🏨 Hôtels & Locations",
        "queries": [
            "hotel boutique paris contact email",
            "chambre d'hôtes provence contact",
            "gite de charme france contact email",
            "conciergerie location saisonnière contact",
            "villa luxe location france contact",
            "hotel restaurant campagne france contact",
        ]
    },
    "restaurants": {
        "label": "🍽️ Restaurants & Traiteurs",
        "queries": [
            "restaurant gastronomique paris contact",
            "traiteur mariage île de france contact email",
            "restaurant bistronomique lyon contact",
            "chef à domicile paris contact",
            "traiteur événementiel bordeaux contact",
            "boulangerie artisanale paris contact",
        ]
    },
    "ecommerce": {
        "label": "🛒 E-commerce & Artisans",
        "queries": [
            "boutique en ligne mode française contact",
            "créateur bijoux france boutique contact",
            "artisan maroquinerie france contact email",
            "marque vêtements made in france contact",
            "boutique déco intérieur en ligne france contact",
            "e-commerce produits artisanaux france",
        ]
    },
    "coaching": {
        "label": "💼 Coaches & Indépendants",
        "queries": [
            "coach business entrepreneur paris contact",
            "consultant marketing digital france contact",
            "photographe professionnel paris contact",
            "coach développement personnel france contact",
            "formateur professionnel indépendant contact",
            "architecte d'intérieur paris contact email",
        ]
    },
}


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.5',
}


def extract_emails(text):
    """Extract and filter email addresses from text."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    raw = re.findall(pattern, text)
    
    blacklist_domains = [
        'example.com', 'test.com', 'email.com', 'domain.com',
        'sentry.io', 'schema.org', 'w3.org', 'googleapis.com',
        'google.com', 'gstatic.com', 'youtube.com', 'facebook.com',
        'twitter.com', 'instagram.com', 'microsoft.com', 'apple.com',
        'amazon.com', 'github.com', 'cloudflare.com', 'jquery.com',
        'wordpress.org', 'wordpress.com', 'w3.org', 'gravatar.com',
        'wix.com', 'squarespace.com', 'shopify.com',
    ]
    blacklist_prefixes = [
        'noreply', 'no-reply', 'unsubscribe', 'mailer-daemon',
        'postmaster', 'webmaster', 'abuse', 'support@wordpress',
        'privacy@', 'gdpr@', 'dpo@',
    ]
    
    valid = []
    for e in raw:
        e = e.lower().strip('.')
        domain = e.split('@')[1] if '@' in e else ''
        
        if any(b in domain for b in blacklist_domains):
            continue
        if any(e.startswith(b) for b in blacklist_prefixes):
            continue
        if len(e) < 7 or len(e) > 60:
            continue
        if e.endswith('.png') or e.endswith('.jpg') or e.endswith('.gif'):
            continue
            
        valid.append(e)
    
    return list(set(valid))


def scrape_contact_page(url):
    """Visit a URL and extract emails. Also looks for /contact page."""
    emails = []
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True)
        if resp.status_code == 200:
            emails.extend(extract_emails(resp.text))
            
            # Also try the /contact page
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Find contact links
            for link in soup.find_all('a', href=True):
                href = link['href'].lower()
                text = link.get_text().lower()
                if 'contact' in href or 'contact' in text:
                    contact_url = href
                    if contact_url.startswith('/'):
                        from urllib.parse import urljoin
                        contact_url = urljoin(url, contact_url)
                    if contact_url.startswith('http'):
                        try:
                            resp2 = requests.get(contact_url, headers=HEADERS, timeout=8)
                            if resp2.status_code == 200:
                                emails.extend(extract_emails(resp2.text))
                        except:
                            pass
                    break  # Only try first contact link
                    
            # Also check for mailto: links
            for link in soup.find_all('a', href=True):
                if 'mailto:' in link['href']:
                    email = link['href'].replace('mailto:', '').split('?')[0].strip()
                    if '@' in email:
                        emails.append(email.lower())
    except:
        pass
    
    return list(set(emails))


def extract_business_name(url):
    """Try to extract a business name from the URL domain."""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        # Remove www.
        domain = domain.replace('www.', '')
        # Get the main name
        name = domain.split('.')[0]
        # Clean up
        name = name.replace('-', ' ').replace('_', ' ').title()
        return name
    except:
        return ""


def find_prospects(industries_filter=None, max_results_per_query=5):
    """Main prospect finding function."""
    
    if not HAS_GSEARCH:
        print("❌ googlesearch-python is required. Run: pip install googlesearch-python")
        return None, []
    
    industries_to_search = industries_filter or list(INDUSTRIES.keys())
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"prospects_{timestamp}.csv")
    
    all_prospects = []
    seen_emails = set()
    seen_domains = set()
    
    print(f"\n{'='*60}")
    print(f"  🚀 PRIME.AI Prospect Finder v3")
    print(f"  Industries: {len(industries_to_search)}")
    print(f"  Strategy: Google Search → Page Scraping → Contact Pages")
    print(f"  Results per query: {max_results_per_query}")
    print(f"{'='*60}")
    
    for ind_key in industries_to_search:
        ind = INDUSTRIES.get(ind_key)
        if not ind:
            continue
        
        print(f"\n{ind['label']}")
        
        for query in ind['queries']:
            print(f"  🔍 {query[:55]}...")
            
            try:
                # Google search - get URLs
                urls = list(gsearch(query, num_results=max_results_per_query, lang="fr"))
            except Exception as e:
                print(f"     ⚠️ Search error: {e}")
                time.sleep(10)  # Longer wait on error
                continue
            
            for url in urls:
                # Skip social media, directories, etc.
                skip = ['google.com', 'facebook.com', 'instagram.com', 'linkedin.com',
                        'twitter.com', 'youtube.com', 'wikipedia.org', 'pagesjaunes.fr',
                        'tripadvisor', 'yelp.com', 'leboncoin.fr']
                if any(s in url for s in skip):
                    continue
                
                # Skip already scraped domains
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc
                except:
                    continue
                    
                if domain in seen_domains:
                    continue
                seen_domains.add(domain)
                
                # Scrape the page
                emails = scrape_contact_page(url)
                business = extract_business_name(url)
                
                for email in emails:
                    if email not in seen_emails:
                        seen_emails.add(email)
                        
                        prospect = {
                            "name": email.split('@')[0].replace('.', ' ').replace('_', ' ').replace('-', ' ').title(),
                            "company": business,
                            "email": email,
                            "industry": ind_key,
                            "city": "",
                            "website": url[:100],
                            "source": query[:50],
                            "found_date": datetime.now().strftime("%Y-%m-%d"),
                        }
                        all_prospects.append(prospect)
                        print(f"     ✅ {email} ({business})")
            
            # Respect Google rate limits
            time.sleep(5)
    
    # Save results
    fieldnames = ["name", "company", "email", "industry", "city", "website", "source", "found_date"]
    with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for p in all_prospects:
            writer.writerow(p)
    
    print(f"\n{'='*60}")
    print(f"  ✅ Prospect Search Complete!")
    print(f"  📊 Total unique emails: {len(all_prospects)}")
    print(f"  🏢 Domains scraped: {len(seen_domains)}")
    print(f"  📄 CSV: {output_csv}")
    print(f"{'='*60}\n")
    
    return output_csv, all_prospects


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("PRIME.AI Prospect Finder v3")
        print("=" * 40)
        print()
        print("Usage:")
        print("  python prospect_finder_v3.py search                  Search ALL")
        print("  python prospect_finder_v3.py search immobilier       One industry")
        print("  python prospect_finder_v3.py search beaute hotels    Multiple")
        print()
        print("Industries:")
        for k, v in INDUSTRIES.items():
            print(f"  {k:20s} {v['label']}")
        sys.exit(0)
    
    cmd = sys.argv[1]
    if cmd == "search":
        ind = sys.argv[2:] if len(sys.argv) > 2 else None
        find_prospects(ind)
    else:
        print(f"Unknown: {cmd}")
