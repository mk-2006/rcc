const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf-8');

// Replace the navigation links globally
const navReplacements = [
    [/<a onclick="switchTab\('home'\)" class="nav-link[^"]*" data-tab="home">Home<\/a>/g, '<a href="index.html" class="nav-link" data-tab="home">Home</a>'],
    [/<a onclick="switchTab\('services'\)" class="nav-link[^"]*" data-tab="services">Services<\/a>/g, '<a href="services.html" class="nav-link" data-tab="services">Services</a>'],
    [/<a onclick="switchTab\('sarkari'\)" class="nav-link[^"]*" data-tab="sarkari">Updates<\/a>/g, '<a href="updates.html" class="nav-link" data-tab="sarkari">Updates</a>'],
    [/<a onclick="switchTab\('contact'\)" class="nav-link[^"]*" data-tab="contact">Contact<\/a>/g, '<a href="contact.html" class="nav-link" data-tab="contact">Contact</a>'],
    
    // Also for mobile nav
    [/<a href="#" onclick="switchTab\('home'\)" class="text-2xl/g, '<a href="index.html" class="text-2xl'],
    [/<a href="#" onclick="switchTab\('home'\)" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"><\/i> Home<\/a>/g, '<a href="index.html" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> Home</a>'],
    [/<a href="#" onclick="switchTab\('sarkari'\)" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"><\/i> View All Update<\/a>/g, '<a href="updates.html" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> View All Update</a>'],
    
    // Homepage buttons
    [/<button onclick="switchTab\('sarkari'\)"/g, '<button onclick="window.location.href=\'updates.html\'"'],
    [/<button onclick="switchTab\('services'\)"/g, '<button onclick="window.location.href=\'services.html\'"']
];

for (const [oldRegex, newText] of navReplacements) {
    html = html.replace(oldRegex, newText);
}

// Update Footer contact info
const footerReplacements = [
    [/Star Cyber Cafe/g, 'Ranjeet Cyber Cafe'],
    [/\+91 80007 77102/g, '+91 6206553454'],
    [/cafe\.star92@gmail\.com/g, 'rcckne@gmail.com'],
    [/Yash Complex\. Nr\. Jalaram Chowk, Gita Mandir Road, Bhaktinagar Circle, Rajkot/g, 'Prem Pul, Kishanganj - 855107']
];

for (const [oldRegex, newText] of footerReplacements) {
    html = html.replace(oldRegex, newText);
}

// Extract major sections
const headEnd = html.indexOf('<body>') + 6;
const head = html.slice(0, headEnd);

const welcomeStart = html.indexOf('<!-- Welcome Animation -->');
const welcomeEnd = html.indexOf('<!-- Background Glows -->');
const welcome = html.slice(welcomeStart, welcomeEnd);

const bgGlowStart = html.indexOf('<!-- Background Glows -->');
const bgGlowEnd = html.indexOf('<!-- Navigation -->');
const bgGlow = html.slice(bgGlowStart, bgGlowEnd);

const navStart = html.indexOf('<!-- Navigation -->');
const navEnd = html.indexOf('<!-- Main Container for Tabs -->');
const nav = html.slice(navStart, navEnd);

const homeSecStart = html.indexOf('<!-- HOME TAB -->');
const servicesSecStart = html.indexOf('<!-- SERVICES TAB -->');
const sarkariSecStart = html.indexOf('<!-- UPDATES TAB (User\'s Code Integrated) -->');
const contactSecStart = html.indexOf('<!-- CONTACT TAB -->');
const mainEnd = html.indexOf('</main>');

const homeSec = html.slice(homeSecStart, servicesSecStart);
const servicesSec = html.slice(servicesSecStart, sarkariSecStart);
const sarkariSec = html.slice(sarkariSecStart, contactSecStart);
const contactSec = html.slice(contactSecStart, mainEnd);

const footerStart = html.indexOf('<!-- Footer -->');
const footerEnd = html.indexOf('<!-- Popup Modal (Fill Open Animation) -->');
const footer = html.slice(footerStart, footerEnd);

const popupStart = footerEnd;
const scripts = html.slice(popupStart);

function makePage(pageName, activeTab, sectionContent, includeWelcome = false) {
    // Set active class on nav
    let pageNav = nav;
    const activeRegex = new RegExp(`class="nav-link" data-tab="${activeTab}"`, 'g');
    pageNav = pageNav.replace(activeRegex, `class="nav-link active" data-tab="${activeTab}"`);
    
    // Ensure section has active class
    let content = sectionContent.replace(/class="page-section"/g, 'class="page-section active"');
    
    let page = head + "\n";
    if (includeWelcome) {
        page += welcome + "\n";
    }
    
    page += bgGlow + "\n";
    page += pageNav + "\n";
    page += '<main class="container mx-auto px-6 py-12 min-h-screen">\n';
    page += content + "\n";
    page += '</main>\n';
    page += footer + "\n";
    
    // Clean up scripts
    let pageScripts = scripts;
    if (!includeWelcome) {
        // Remove welcome animation timeout from scripts using regex
        pageScripts = pageScripts.replace(/setTimeout\(\(\) => {[\s\S]*?}, 2200\);/g, '');
    }
    
    // Remove switchTab function
    pageScripts = pageScripts.replace(/\/\/ 2\. SPA Tab Switching Logic[\s\S]*?\/\/ 3\. Mobile Menu Toggle/, '// 3. Mobile Menu Toggle');
    
    page += pageScripts;
    
    fs.writeFileSync(pageName, page, 'utf-8');
}

makePage('index.html', 'home', homeSec, true);
makePage('services.html', 'services', servicesSec, false);
makePage('updates.html', 'sarkari', sarkariSec, false);
makePage('contact.html', 'contact', contactSec, false);

console.log("Split completed successfully!");
