import os
import re

files = ['index.html', 'services.html', 'updates.html', 'contact.html', 'booking.html']

css_addition = """
/* Animated Hamburger & Menu */
#mobile-toggle-btn span {
    display: block;
    width: 24px;
    height: 2px;
    background: #cbd5e1;
    transition: all 0.3s ease-in-out;
    border-radius: 2px;
}
#mobile-toggle-btn.hamburger-open span:nth-child(1) {
    transform: translateY(8px) rotate(45deg);
}
#mobile-toggle-btn.hamburger-open span:nth-child(2) {
    opacity: 0;
}
#mobile-toggle-btn.hamburger-open span:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg);
}

#mobile-menu {
    transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    max-height: 0;
    opacity: 0;
    overflow: hidden;
}
#mobile-menu.menu-open {
    max-height: 500px; /* Large enough to contain the menu */
    opacity: 1;
}
"""

js_addition = """
    // Mobile Menu Toggle with Outside Click
    function toggleMobileMenu(event) {
        if(event) event.stopPropagation();
        const menu = document.getElementById('mobile-menu');
        const btn = document.getElementById('mobile-toggle-btn');
        
        menu.classList.toggle('menu-open');
        btn.classList.toggle('hamburger-open');
        
        // Remove hidden if it's there
        if(menu.classList.contains('hidden')) {
            menu.classList.remove('hidden');
        }
    }

    document.addEventListener("click", function(event) {
        const menu = document.getElementById('mobile-menu');
        const btn = document.getElementById('mobile-toggle-btn');
        if (menu && btn && menu.classList.contains('menu-open')) {
            if (!menu.contains(event.target) && !btn.contains(event.target)) {
                menu.classList.remove('menu-open');
                btn.classList.remove('hamburger-open');
            }
        }
    });
"""

for file in files:
    if not os.path.exists(file):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject CSS
    if '/* Animated Hamburger & Menu */' not in content:
        content = content.replace('/* Navbar */', css_addition + '\n/* Navbar */')

    # 2. Replace Hamburger Button
    old_btn = '<button class="md:hidden text-2xl text-slate-300 focus:outline-none" onclick="toggleMobileMenu()">'
    new_btn = '<button id="mobile-toggle-btn" class="md:hidden flex flex-col justify-center items-center w-8 h-8 focus:outline-none gap-1.5 z-50" onclick="toggleMobileMenu(event)">'
    if old_btn in content:
        # replace the button and the icon
        content = re.sub(
            r'<button class="md:hidden text-2xl text-slate-300 focus:outline-none" onclick="toggleMobileMenu\(\)">\s*<i class="fa-solid fa-bars"></i>\s*</button>',
            new_btn + '\n            <span></span>\n            <span></span>\n            <span></span>\n        </button>',
            content
        )

    # 3. Replace mobile menu classes
    old_menu = '<div id="mobile-menu" class="hidden md:hidden bg-slate-900 border-t border-slate-800 mt-4 absolute w-full left-0 shadow-2xl z-50">'
    new_menu = '<div id="mobile-menu" class="md:hidden bg-slate-900 border-t border-slate-800 mt-4 absolute w-full left-0 shadow-2xl z-50 top-full">'
    if old_menu in content:
        content = content.replace(old_menu, new_menu)
    # Also handle if it's already modified
    old_menu_2 = '<div id="mobile-menu" class="md:hidden bg-slate-900/95 backdrop-blur-xl border-t border-slate-800 mt-4 absolute w-full left-0 shadow-[0_20px_40px_rgba(0,0,0,0.8)] z-50 mobile-menu-closed rounded-b-2xl">'
    new_menu_2 = '<div id="mobile-menu" class="md:hidden bg-slate-900/95 backdrop-blur-xl border-t border-slate-800 mt-4 absolute w-full left-0 shadow-[0_20px_40px_rgba(0,0,0,0.8)] z-50 top-full rounded-b-2xl">'
    if old_menu_2 in content:
        content = content.replace(old_menu_2, new_menu_2)

    # 4. Replace JS
    # Find the old toggle function
    old_js_pattern = re.compile(r'function toggleMobileMenu\(\) \{[\s\S]*?\}', re.MULTILINE)
    if 'toggleMobileMenu(event)' not in content:
        content = old_js_pattern.sub(js_addition, content, count=1)

    # 5. Updates page specific fixes
    if file == 'updates.html':
        content = content.replace(
            '<a href="${item.link}" target="_blank" class="px-5 py-2.5 bg-cyan-600 text-white font-bold rounded-lg hover:bg-cyan-500 transition text-sm flex items-center gap-2 shadow-[0_0_10px_rgba(0,255,255,0.2)]">',
            '<button onclick="openPopup(\'Ranjeet Cyber Cafe\', \'Visit our cafe to know full details about this job / result.\\n\\nOnline Forms • Admit Card • Results • Fast Internet\')" class="px-5 py-2.5 bg-cyan-600 text-white font-bold rounded-lg hover:bg-cyan-500 transition text-sm flex items-center gap-2 shadow-[0_0_10px_rgba(0,255,255,0.2)]">'
        )
        content = content.replace(
            'View Details <i class="fa-solid fa-arrow-right"></i>\n                    </a>',
            'View Details <i class="fa-solid fa-arrow-right"></i>\n                    </button>'
        )
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updates applied.")
