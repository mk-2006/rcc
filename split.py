import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the navigation links globally
nav_replacements = [
    (r'<a onclick="switchTab\(\'home\'\)" class="nav-link[^"]*" data-tab="home">Home</a>', r'<a href="index.html" class="nav-link" data-tab="home">Home</a>'),
    (r'<a onclick="switchTab\(\'services\'\)" class="nav-link[^"]*" data-tab="services">Services</a>', r'<a href="services.html" class="nav-link" data-tab="services">Services</a>'),
    (r'<a onclick="switchTab\(\'sarkari\'\)" class="nav-link[^"]*" data-tab="sarkari">Updates</a>', r'<a href="updates.html" class="nav-link" data-tab="sarkari">Updates</a>'),
    (r'<a onclick="switchTab\(\'contact\'\)" class="nav-link[^"]*" data-tab="contact">Contact</a>', r'<a href="contact.html" class="nav-link" data-tab="contact">Contact</a>'),
    
    # Also for mobile nav
    (r'<a href="#" onclick="switchTab\(\'home\'\)" class="text-2xl', r'<a href="index.html" class="text-2xl'),
    (r'<a href="#" onclick="switchTab\(\'home\'\)" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> Home</a>', r'<a href="index.html" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> Home</a>'),
    (r'<a href="#" onclick="switchTab\(\'sarkari\'\)" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> View All Update</a>', r'<a href="updates.html" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> View All Update</a>'),
    
    # Homepage buttons
    (r'<button onclick="switchTab\(\'sarkari\'\)"', r'<button onclick="window.location.href=\'updates.html\'"'),
    (r'<button onclick="switchTab\(\'services\'\)"', r'<button onclick="window.location.href=\'services.html\'"')
]

for old, new in nav_replacements:
    html = re.sub(old, new, html)

# Update Footer contact info
footer_replacements = [
    (r'Star Cyber Cafe', r'Ranjeet Cyber Cafe'),
    (r'\+91 80007 77102', r'+91 6206553454'),
    (r'cafe\.star92@gmail\.com', r'rcckne@gmail.com'),
    (r'Yash Complex\. Nr\. Jalaram Chowk, Gita Mandir Road, Bhaktinagar Circle, Rajkot', r'Prem Pul, Kishanganj - 855107')
]

# Only replace footer occurrences, but wait, doing globally is fine because the old contact details only exist there now, or we can just run it globally.
for old, new in footer_replacements:
    html = re.sub(old, new, html)

# Extract major sections
head_end = html.find('<body>') + 6
head = html[:head_end]

welcome_start = html.find('<!-- Welcome Animation -->')
welcome_end = html.find('<!-- Background Glows -->')
welcome = html[welcome_start:welcome_end]

bg_glow_start = html.find('<!-- Background Glows -->')
bg_glow_end = html.find('<!-- Navigation -->')
bg_glow = html[bg_glow_start:bg_glow_end]

nav_start = html.find('<!-- Navigation -->')
nav_end = html.find('<!-- Main Container for Tabs -->')
nav = html[nav_start:nav_end]

main_start = html.find('<main class="container mx-auto px-6 py-12 min-h-screen">') + len('<main class="container mx-auto px-6 py-12 min-h-screen">')

home_sec_start = html.find('<!-- HOME TAB -->')
services_sec_start = html.find('<!-- SERVICES TAB -->')
sarkari_sec_start = html.find('<!-- UPDATES TAB (User\'s Code Integrated) -->')
contact_sec_start = html.find('<!-- CONTACT TAB -->')
main_end = html.find('</main>')

home_sec = html[home_sec_start:services_sec_start]
services_sec = html[services_sec_start:sarkari_sec_start]
sarkari_sec = html[sarkari_sec_start:contact_sec_start]
contact_sec = html[contact_sec_start:main_end]

footer_start = html.find('<!-- Footer -->')
footer_end = html.find('<!-- Popup Modal (Fill Open Animation) -->')
footer = html[footer_start:footer_end]

popup_start = footer_end
scripts_end = len(html)
scripts = html[popup_start:scripts_end]

def make_page(page_name, active_tab, section_content, include_welcome=False):
    # Set active class on nav
    page_nav = nav
    page_nav = page_nav.replace(f'data-tab="{active_tab}">', f'data-tab="{active_tab}" class="nav-link active">')
    # Actually, the regex removed the active class, let\'s add it carefully.
    page_nav = re.sub(f\'class="nav-link" data-tab="{active_tab}"\', f\'class="nav-link active" data-tab="{active_tab}"\', page_nav)
    
    # Ensure section has active class
    section_content = section_content.replace('class="page-section"', 'class="page-section active"')
    
    page = head + "\n"
    if include_welcome:
        page += welcome + "\n"
    
    page += bg_glow + "\n"
    page += page_nav + "\n"
    page += '<main class="container mx-auto px-6 py-12 min-h-screen">\n'
    page += section_content + "\n"
    page += '</main>\n'
    page += footer + "\n"
    
    # Clean up scripts
    page_scripts = scripts
    if not include_welcome:
        # Remove welcome animation timeout from scripts
        page_scripts = re.sub(r'setTimeout\(\(\) => {\s*const welcome = document.getElementById\(\'welcome-screen\'\);.*?\}, 2200\);', '', page_scripts, flags=re.DOTALL)
    
    # Remove switchTab function
    page_scripts = re.sub(r'// 2\. SPA Tab Switching Logic.*?// 3\. Mobile Menu Toggle', '// 3. Mobile Menu Toggle', page_scripts, flags=re.DOTALL)
    
    page += page_scripts
    
    with open(page_name, 'w', encoding='utf-8') as out_f:
        out_f.write(page)

make_page('index.html', 'home', home_sec, include_welcome=True)
make_page('services.html', 'services', services_sec, include_welcome=False)
make_page('updates.html', 'sarkari', sarkari_sec, include_welcome=False)
make_page('contact.html', 'contact', contact_sec, include_welcome=False)

print("Split completed successfully!")
