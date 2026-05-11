$files = @("index.html", "services.html", "updates.html", "contact.html")

foreach ($file in $files) {
    $content = Get-Content -Raw $file
    
    # Change About Us to About Me and link to index.html#about-me
    $content = $content -replace '<a href="#" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> About Us</a>', '<a href="index.html#about-me" class="hover:text-cyan-400 transition flex items-center gap-2"><i class="fa-solid fa-angle-right text-xs"></i> About Me</a>'
    
    # Change fa-star to fa-microchip
    $content = $content -replace '<i class="fa-solid fa-star text-cyan-400"></i>', '<i class="fa-solid fa-microchip text-cyan-400"></i>'
    
    # Add scroll-behavior: smooth
    $content = $content -replace '/\* Base Styles \*/\s*body \{', "/* Base Styles */`r`nhtml { scroll-behavior: smooth; }`r`nbody {"
    
    # Add id="about-me" to the About Me section in index.html
    if ($file -eq "index.html") {
        $content = $content -replace '<!-- ABOUT US SECTION -->\s*<div class="mt-10 border-t border-slate-800 pt-20 pb-10">', '<!-- ABOUT ME SECTION -->`r`n        <div id="about-me" class="mt-10 border-t border-slate-800 pt-20 pb-10">'
    }

    [IO.File]::WriteAllText("c:\Users\user\.gemini\antigravity\scratch\ranjeet-cyber-cafe\" + $file, $content)
}

Write-Output "Updates completed!"
