import zipfile, os

zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PRIMEAI_prospects.zip")
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prospects_20260219_0223.csv")
html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "email_preview.html")

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    if os.path.exists(csv_path):
        zf.write(csv_path, "prospects_300.csv")
        print(f"Added CSV: {os.path.getsize(csv_path)} bytes")
    if os.path.exists(html_path):
        zf.write(html_path, "email_preview.html")
        print(f"Added HTML: {os.path.getsize(html_path)} bytes")

print(f"ZIP created: {zip_path}")
print(f"ZIP size: {os.path.getsize(zip_path)} bytes")
