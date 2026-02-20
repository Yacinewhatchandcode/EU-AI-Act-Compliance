"""
Convert prospects CSV to YAML format + enrich via Google search for real contact info.
Uses real Google search scraping in a browser for better results.
"""
import csv
import os
import re
import sys
import json
import time
import yaml
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'fr-FR,fr;q=0.9',
}

BLACKLIST = ['example.com', 'google.com', 'facebook.com', 'twitter.com',
    'instagram.com', 'youtube.com', 'linkedin.com', 'gstatic.com',
    'w3.org', 'schema.org', 'jquery.com', 'gravatar.com', 'wordpress.org',
    'sentry.io', 'cloudflare.com']


def find_emails(text):
    raw = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return list(set(e.lower() for e in raw 
        if not any(b in e for b in BLACKLIST)
        and not e.startswith(('noreply', 'no-reply', 'unsubscribe', 'webmaster'))
        and not e.endswith(('.png', '.jpg', '.gif', '.css', '.js'))))


def find_linkedin(text):
    return list(set(
        re.findall(r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[a-zA-Z0-9_-]+/?', text)
    ))


def find_phones(text):
    phones = re.findall(r'(?:0|\+33)\s*[1-9](?:[\s.-]*\d{2}){4}', text)
    return [p.strip() for p in phones][:3]


def scrape_website(url):
    """Scrape a website for email, phone, linkedin."""
    result = {"emails": [], "linkedin": [], "phones": []}
    try:
        r = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True)
        if r.status_code != 200:
            return result
        
        text = r.text
        result["emails"] = find_emails(text)
        result["linkedin"] = find_linkedin(text)
        result["phones"] = find_phones(text)
        
        # Try /contact page
        soup = BeautifulSoup(text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href'].lower()
            label = (a.get_text() or '').lower()
            if 'mailto:' in a['href']:
                em = a['href'].replace('mailto:', '').split('?')[0].strip()
                if '@' in em:
                    result["emails"].append(em.lower())
            if 'linkedin.com' in a['href']:
                result["linkedin"].append(a['href'])
            if 'contact' in href or 'contact' in label:
                contact_url = a['href']
                if contact_url.startswith('/'):
                    contact_url = urljoin(url, contact_url)
                if contact_url.startswith('http') and contact_url != url:
                    try:
                        r2 = requests.get(contact_url, headers=HEADERS, timeout=5)
                        if r2.status_code == 200:
                            result["emails"].extend(find_emails(r2.text))
                            result["linkedin"].extend(find_linkedin(r2.text))
                            result["phones"].extend(find_phones(r2.text))
                    except:
                        pass
                    break
        
        result["emails"] = list(set(result["emails"]))[:3]
        result["linkedin"] = list(set(result["linkedin"]))[:2]
        result["phones"] = list(set(result["phones"]))[:2]
    except:
        pass
    return result


def search_and_scrape(name, city, siren=""):
    """Use Google via requests to find website, then scrape it."""
    result = {"website": "", "emails": [], "linkedin": [], "phones": []}
    
    # First try annuaire-entreprises for website
    if siren:
        try:
            api_url = f"https://recherche-entreprises.api.gouv.fr/search?q={siren}&page=1&per_page=1"
            r = requests.get(api_url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                results = data.get("results", [])
                if results:
                    complements = results[0].get("complements", {})
                    site = complements.get("site_web", "")
                    if site:
                        result["website"] = site if site.startswith("http") else f"https://{site}"
        except:
            pass
    
    # If no website from API, try PagesJaunes search
    if not result["website"]:
        try:
            pj_url = f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={quote_plus(name)}&ou={quote_plus(city)}"
            r = requests.get(pj_url, headers=HEADERS, timeout=8)
            if r.status_code == 200:
                result["emails"].extend(find_emails(r.text))
                result["phones"].extend(find_phones(r.text))
                # Get website links
                soup = BeautifulSoup(r.text, 'html.parser')
                for a in soup.find_all('a', href=True):
                    if 'linkedin.com' in a['href']:
                        result["linkedin"].append(a['href'])
        except:
            pass
    
    # Scrape website if found
    if result["website"]:
        site_data = scrape_website(result["website"])
        result["emails"].extend(site_data["emails"])
        result["linkedin"].extend(site_data["linkedin"])
        result["phones"].extend(site_data["phones"])
    
    # Deduplicate
    result["emails"] = list(set(result["emails"]))[:3]
    result["linkedin"] = list(set(result["linkedin"]))[:2]
    result["phones"] = list(set(result["phones"]))[:2]
    
    return result


def main(csv_path, max_enrich=300):
    # Read CSV
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        prospects = list(csv.DictReader(f, delimiter=";"))
    
    print(f"\n{'='*60}")
    print(f"  🔧 PRIME.AI Prospect Enricher v2")
    print(f"  📊 Total: {len(prospects)} prospects")
    print(f"  🔍 Enriching: {min(max_enrich, len(prospects))}")
    print(f"{'='*60}\n")
    
    # Build YAML structure
    yaml_data = {
        "meta": {
            "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_prospects": len(prospects),
            "service": "PRIME.AI - AI Visual Content",
            "target_market": "France"
        },
        "industries": {}
    }
    
    enriched = 0
    
    for i, p in enumerate(prospects):
        industry = p.get("industry", "other")
        name = p.get("name", "")
        city = p.get("city", "")
        siren = p.get("siren", "")
        
        if industry not in yaml_data["industries"]:
            yaml_data["industries"][industry] = []
        
        entry = {
            "name": name,
            "siren": siren,
            "city": city,
            "postal_code": p.get("postal_code", ""),
            "address": p.get("address", ""),
            "email": p.get("email", ""),
            "phone": p.get("phone", ""),
            "website": p.get("website", ""),
            "linkedin": "",
        }
        
        # Enrich
        if i < max_enrich and not entry["email"]:
            print(f"  [{i+1}/{len(prospects)}] {name[:45]:45s} ({city[:20]})...", end=" ", flush=True)
            try:
                info = search_and_scrape(name, city, siren)
                
                found = []
                if info["emails"]:
                    entry["email"] = info["emails"][0]
                    found.append(f"📧 {info['emails'][0]}")
                    enriched += 1
                if info["linkedin"]:
                    entry["linkedin"] = info["linkedin"][0]
                    found.append("🔗 LinkedIn")
                if info["website"]:
                    entry["website"] = info["website"]
                    found.append(f"🌐 site")
                if info["phones"]:
                    entry["phone"] = info["phones"][0]
                    found.append(f"📞 tel")
                
                if found:
                    print(" | ".join(found))
                else:
                    print("❌")
            except Exception as e:
                print(f"⚠️ {str(e)[:50]}")
            
            time.sleep(0.5)
        
        yaml_data["industries"][industry].append(entry)
    
    # Save YAML
    base = os.path.dirname(os.path.abspath(csv_path))
    yaml_path = os.path.join(base, "prospects.yaml")
    
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=200)
    
    print(f"\n{'='*60}")
    print(f"  ✅ Done!")
    print(f"  📧 Emails found: {enriched}")
    print(f"  📄 YAML saved: {yaml_path}")
    print(f"  📦 Size: {os.path.getsize(yaml_path)} bytes")
    print(f"{'='*60}\n")
    
    return yaml_path


if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "prospects_20260219_0223.csv")
    max_e = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    main(csv_file, max_e)
