import os
import re

files = ['index.html', 'services.html', 'updates.html', 'contact.html', 'booking.html']

css_addition = """/* Animation Improvements */
.mobile-menu-closed {
    opacity: 0;
    transform: translateY(-20px) scale(0.98);
    pointer-events: none;
    visibility: hidden;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.mobile-menu-open {
    opacity: 1;
    transform: translateY(0) scale(1);
    pointer-events: auto;
    visibility: visible;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.mobile-nav-link {
    transition: all 0.2s ease;
    display: block;
    transform-origin: left;
}
.mobile-nav-link:active {
    transform: scale(0.95);
    color: #00ffff;
}
button:active {
    transform: scale(0.95) !important;
    transition: transform 0.1s !important;
}
.card:active {
    transform: scale(0.98) translateY(0) !important;
    transition: transform 0.1s !important;
}
"""

old_js = """    // 3. Mobile Menu Toggle
    function toggleMobileMenu() {
        const menu = document.getElementById('mobile-menu');
        menu.classList.toggle('hidden');
    }"""

new_js = """    // 3. Mobile Menu Toggle
    function toggleMobileMenu() {
        const menu = document.getElementById('mobile-menu');
        const icon = document.querySelector('#mobile-toggle-btn i');
        
        if (menu.classList.contains('mobile-menu-closed')) {
            menu.classList.remove('mobile-menu-closed');
            menu.classList.add('mobile-menu-open');
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-xmark');
            icon.parentElement.style.transform = 'rotate(90deg)';
        } else {
            menu.classList.remove('mobile-menu-open');
            menu.classList.add('mobile-menu-closed');
            icon.classList.remove('fa-xmark');
            icon.classList.add('fa-bars');
            icon.parentElement.style.transform = 'rotate(0deg)';
        }
    }"""

for file in files:
    if not os.path.exists(file):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    if '/* Animation Improvements */' not in content:
        content = content.replace('/* Navbar */', css_addition + '\n/* Navbar */')

    content = content.replace(
        '<button class="md:hidden text-2xl text-slate-300 focus:outline-none" onclick="toggleMobileMenu()">',
        '<button id="mobile-toggle-btn" class="md:hidden text-2xl text-slate-300 focus:outline-none transition-transform duration-300 hover:scale-110" onclick="toggleMobileMenu()">'
    )

    content = content.replace(
        '<div id="mobile-menu" class="hidden md:hidden bg-slate-900 border-t border-slate-800 mt-4 absolute w-full left-0 shadow-2xl z-50">',
        '<div id="mobile-menu" class="md:hidden bg-slate-900/95 backdrop-blur-xl border-t border-slate-800 mt-4 absolute w-full left-0 shadow-[0_20px_40px_rgba(0,0,0,0.8)] z-50 mobile-menu-closed rounded-b-2xl">'
    )

    parts = content.split('<!-- Mobile Nav -->')
    if len(parts) > 1:
        mobile_nav = parts[1]
        mobile_nav = mobile_nav.replace('class="nav-link active"', 'class="nav-link active mobile-nav-link text-lg"')
        mobile_nav = mobile_nav.replace('class="nav-link"', 'class="nav-link mobile-nav-link text-lg"')
        mobile_nav = mobile_nav.replace('class="text-violet-400"', 'class="text-violet-400 mobile-nav-link text-lg font-bold"')
        content = parts[0] + '<!-- Mobile Nav -->' + mobile_nav

    content = content.replace(old_js, new_js)

    content = content.replace(
        'hover:bg-violet-500 transition shadow-[0_0_10px_rgba(139,92,246,0.4)]',
        'hover:bg-violet-500 transition-all duration-300 hover:scale-105 shadow-[0_0_10px_rgba(139,92,246,0.4)] hover:shadow-[0_0_20px_rgba(139,92,246,0.6)]'
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated animations in {len(files)} files.")
