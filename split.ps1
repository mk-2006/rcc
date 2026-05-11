$html = Get-Content -Raw "index.html"

# Replace Nav Links
$html = $html -replace '<a onclick="switchTab\(''home''\)" class="nav-link[^"]*" data-tab="home">Home</a>', '<a href="index.html" class="nav-link" data-tab="home">Home</a>'
$html = $html -replace '<a onclick="switchTab\(''services''\)" class="nav-link[^"]*" data-tab="services">Services</a>', '<a href="services.html" class="nav-link" data-tab="services">Services</a>'
$html = $html -replace '<a onclick="switchTab\(''sarkari''\)" class="nav-link[^"]*" data-tab="sarkari">Updates</a>', '<a href="updates.html" class="nav-link" data-tab="sarkari">Updates</a>'
$html = $html -replace '<a onclick="switchTab\(''contact''\)" class="nav-link[^"]*" data-tab="contact">Contact</a>', '<a href="contact.html" class="nav-link" data-tab="contact">Contact</a>'

# Replace Mobile Nav Header Link & Quick Links
$html = $html -replace '<a href="#" onclick="switchTab\(''home''\)" class="text-2xl', '<a href="index.html" class="text-2xl'
$html = $html -replace '<a href="#" onclick="switchTab\(''home''\)" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> Home</a>', '<a href="index.html" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> Home</a>'
$html = $html -replace '<a href="#" onclick="switchTab\(''sarkari''\)" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> View All Update</a>', '<a href="updates.html" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> View All Update</a>'

# Homepage buttons
$html = $html -replace '<button onclick="switchTab\(''sarkari''\)"', '<button onclick="window.location.href=''updates.html''"'
$html = $html -replace '<button onclick="switchTab\(''services''\)"', '<button onclick="window.location.href=''services.html''"'

# Update Contact Info in Footer
$html = $html -replace 'Star Cyber Cafe', 'Ranjeet Cyber Cafe'
$html = $html -replace '\+91 80007 77102', '+91 6206553454'
$html = $html -replace 'cafe\.star92@gmail\.com', 'rcckne@gmail.com'
$html = $html -replace 'Yash Complex\. Nr\. Jalaram Chowk, Gita Mandir Road, Bhaktinagar Circle, Rajkot', 'Prem Pul, Kishanganj - 855107'

# Find Sections
$headEnd = $html.IndexOf('<body>') + 6
$head = $html.Substring(0, $headEnd)

$welcomeStart = $html.IndexOf('<!-- Welcome Animation -->')
$welcomeEnd = $html.IndexOf('<!-- Background Glows -->')
$welcome = $html.Substring($welcomeStart, $welcomeEnd - $welcomeStart)

$bgGlowStart = $html.IndexOf('<!-- Background Glows -->')
$bgGlowEnd = $html.IndexOf('<!-- Navigation -->')
$bgGlow = $html.Substring($bgGlowStart, $bgGlowEnd - $bgGlowStart)

$navStart = $html.IndexOf('<!-- Navigation -->')
$navEnd = $html.IndexOf('<!-- Main Container for Tabs -->')
$nav = $html.Substring($navStart, $navEnd - $navStart)

$homeSecStart = $html.IndexOf('<!-- HOME TAB -->')
$servicesSecStart = $html.IndexOf('<!-- SERVICES TAB -->')
$sarkariSecStart = $html.IndexOf('<!-- UPDATES TAB (User''s Code Integrated) -->')
$contactSecStart = $html.IndexOf('<!-- CONTACT TAB -->')
$mainEnd = $html.IndexOf('</main>')

$homeSec = $html.Substring($homeSecStart, $servicesSecStart - $homeSecStart)
$servicesSec = $html.Substring($servicesSecStart, $sarkariSecStart - $servicesSecStart)
$sarkariSec = $html.Substring($sarkariSecStart, $contactSecStart - $sarkariSecStart)
$contactSec = $html.Substring($contactSecStart, $mainEnd - $contactSecStart)

$footerStart = $html.IndexOf('<!-- Footer -->')
$footerEnd = $html.IndexOf('<!-- Popup Modal \(Fill Open Animation\) -->')
if ($footerEnd -eq -1) {
    # Try exact match without escape if regex was failing
    $footerEnd = $html.IndexOf('<!-- Popup Modal (Fill Open Animation) -->')
}
$footer = $html.Substring($footerStart, $footerEnd - $footerStart)

$popupStart = $footerEnd
$scripts = $html.Substring($popupStart)

function Make-Page {
    param($pageName, $activeTab, $sectionContent, $includeWelcome)

    $pageNav = $nav -replace "class=`"nav-link`" data-tab=`"$activeTab`"", "class=`"nav-link active`" data-tab=`"$activeTab`""
    $content = $sectionContent -replace 'class="page-section"', 'class="page-section active"'
    
    $page = $head + "`r`n"
    if ($includeWelcome) {
        $page += $welcome + "`r`n"
    }
    
    $page += $bgGlow + "`r`n"
    $page += $pageNav + "`r`n"
    $page += '<main class="container mx-auto px-6 py-12 min-h-screen">' + "`r`n"
    $page += $content + "`r`n"
    $page += '</main>' + "`r`n"
    $page += $footer + "`r`n"
    
    $pageScripts = $scripts
    if (-not $includeWelcome) {
        $pageScripts = $pageScripts -replace '(?s)setTimeout\(\(\) => \{.*?\}, 2200\);', ''
    }
    
    $pageScripts = $pageScripts -replace '(?s)// 2\. SPA Tab Switching Logic.*?// 3\. Mobile Menu Toggle', '// 3. Mobile Menu Toggle'
    
    $page += $pageScripts
    
    [IO.File]::WriteAllText("c:\Users\user\.gemini\antigravity\scratch\ranjeet-cyber-cafe\" + $pageName, $page)
}

Make-Page -pageName 'index.html' -activeTab 'home' -sectionContent $homeSec -includeWelcome $true
Make-Page -pageName 'services.html' -activeTab 'services' -sectionContent $servicesSec -includeWelcome $false
Make-Page -pageName 'updates.html' -activeTab 'sarkari' -sectionContent $sarkariSec -includeWelcome $false
Make-Page -pageName 'contact.html' -activeTab 'contact' -sectionContent $contactSec -includeWelcome $false

Write-Output "Split completed successfully!"
