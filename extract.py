import urllib.request
import re
import json

url = "https://www.sarkariexam.com/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    
    # regex to find headers
    # <h4 class="wp-block-heading has-text-align-center"><strong>Result</strong></h4>
    pattern = r'<h4[^>]*>.*?<strong>(.*?)</strong>.*?</h4>(.*?)(?=<h4|<div class="wp-block-columns|$)'
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
    
    extracted = {}
    for header, content in matches:
        # find all list items
        links = re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', content)
        if links:
            if header not in extracted:
                extracted[header] = []
            for href, title in links:
                title = re.sub(r'<[^>]+>', '', title).strip()
                extracted[header].append({"title": title, "url": href})
                
    # Also look for breaking news
    breaking = re.findall(r'<div class="brack-text-rigt"><a[^>]*href="([^"]+)"[^>]*>(.*?)</a></div>', html)
    if breaking:
        extracted["Breaking News"] = [{"title": re.sub(r'<[^>]+>', '', t).strip(), "url": h} for h, t in breaking]

    with open('c:\\Users\\user\\.gemini\\antigravity\\scratch\\ranjeet-cyber-cafe\\extracted_data.json', 'w', encoding='utf-8') as f:
        json.dump(extracted, f, indent=4)
        
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")
