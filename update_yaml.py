"""Update prospects.yaml with enriched contact data from web research."""
import yaml, os

yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prospects.yaml")

with open(yaml_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# Enrichment data from web research
enrichments = {
    # Hotels
    "B & B Hotels France": {"email": "ventes.loisirs@hotelbb.com", "website": "https://www.hotel-bb.com", "linkedin": "https://www.linkedin.com/company/b-b-hotels/"},
    "Les Hotels De Paris (Machefert Group)": {"email": "info@machefert.com", "phone": "+33 1 55 73 75 75", "website": "https://www.leshotelsdeparis.com", "linkedin": "https://www.linkedin.com/company/machefert-group/"},
    "Okko Hotels (Okko Realisations)": {"email": "contact@okkohotels.com", "website": "https://www.okkohotels.com", "linkedin": "https://www.linkedin.com/company/okko-hotels/"},
    "Hotel Alpaga (Epm)": {"email": "alpaga@beaumier.com", "website": "https://www.alpaga.com", "linkedin": ""},
    "Vacances Bleues Hotels": {"email": "info@vacancesbleues.fr", "website": "https://www.vacancesbleues.fr", "linkedin": "https://www.linkedin.com/company/vacances-bleues/"},
    "Lemon Hotels (Lemon Formations)": {"email": "", "website": "https://www.hotel-lemon.com", "phone": "+33 4 93 28 63 63"},
    "Hold Hotels (Hold Hotels)": {"email": "", "website": "", "linkedin": ""},
    
    # Restaurants
    "Big Mamma Restaurants France": {"email": "privacy@bigmamma.com", "website": "https://www.bigmammagroup.com", "linkedin": "https://www.linkedin.com/company/big-mamma-group/"},
    "Crocodile Restaurants": {"email": "info@colmar.be", "website": "https://www.restaurantscrocodile.fr", "linkedin": "https://www.linkedin.com/company/restaurants-crocodile/"},
    "Restaurant La Matelote": {"email": "contact@la-matelote.com", "phone": "+33 3 21 30 17 97", "website": "https://www.la-matelote.com"},
    
    # Immobilier
    "Soliha Agence Immobiliere Sociale Bretagne (Soliha Ais Bretagne)": {"email": "ais.bretagne@soliha.fr", "website": "https://www.soliha-ais-bretagne.fr", "linkedin": "https://www.linkedin.com/company/soliha-ais-bretagne/", "phone": "02 96 61 14 41"},
}

updated = 0
for industry, prospects in data["industries"].items():
    for p in prospects:
        name = p.get("name", "")
        if name in enrichments:
            for k, v in enrichments[name].items():
                if v:
                    p[k] = v
            updated += 1
            print(f"  ✅ {name}: {enrichments[name].get('email', 'N/A')}")

# Save
with open(yaml_path, 'w', encoding='utf-8') as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=200)

print(f"\n✅ Updated {updated} prospects in {yaml_path}")
print(f"📦 Size: {os.path.getsize(yaml_path)} bytes")
