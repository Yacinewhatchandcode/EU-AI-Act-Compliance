"""Convert prospects CSV to YAML - direct conversion, no web scraping."""
import csv, os, yaml
from datetime import datetime

csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prospects_20260219_0223.csv")

with open(csv_path, "r", encoding="utf-8-sig") as f:
    prospects = list(csv.DictReader(f, delimiter=";"))

yaml_data = {
    "meta": {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_prospects": len(prospects),
        "service": "PRIME.AI - AI Visual Content",
        "target_market": "France",
        "industries_covered": ["immobilier", "beaute", "hotels", "restaurants", "ecommerce", "coaching"],
    },
    "industries": {}
}

for p in prospects:
    ind = p.get("industry", "other")
    if ind not in yaml_data["industries"]:
        yaml_data["industries"][ind] = []
    yaml_data["industries"][ind].append({
        "name": p.get("name", ""),
        "siren": p.get("siren", ""),
        "address": p.get("address", ""),
        "city": p.get("city", ""),
        "postal_code": p.get("postal_code", ""),
        "email": p.get("email", ""),
        "phone": p.get("phone", ""),
        "website": p.get("website", ""),
        "linkedin": "",
    })

# Count per industry
for ind, items in yaml_data["industries"].items():
    print(f"  {ind}: {len(items)} prospects")

yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prospects.yaml")
with open(yaml_path, "w", encoding="utf-8") as f:
    yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=200)

print(f"\n✅ YAML saved: {yaml_path}")
print(f"📦 Size: {os.path.getsize(yaml_path)} bytes")
