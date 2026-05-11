const https = require('https');
const fs = require('fs');

const url = "https://www.sarkariexam.com/";

https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        const extracted = {};
        
        // Find breaking news
        const breakingMatch = [...data.matchAll(/<div class="brack-text-rigt"><a[^>]*href="([^"]+)"[^>]*>(.*?)<\/a><\/div>/g)];
        if (breakingMatch.length > 0) {
            extracted["Breaking News"] = breakingMatch.map(m => ({ title: m[2].replace(/<[^>]+>/g, '').trim(), url: m[1] }));
        }

        const sections = [...data.matchAll(/<h4[^>]*>.*?<strong>(.*?)<\/strong>.*?<\/h4>(.*?)<\/ul>/gis)];
        for (const match of sections) {
            const header = match[1];
            const content = match[2];
            
            const links = [];
            const linkMatches = [...content.matchAll(/<li[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)<\/a><\/li>/gi)];
            for (const lmatch of linkMatches) {
                const title = lmatch[2].replace(/<[^>]+>/g, '').trim();
                const href = lmatch[1];
                if (title && href) {
                    links.push({ title, url: href });
                }
            }
            if (links.length > 0) {
                if (!extracted[header]) extracted[header] = [];
                extracted[header].push(...links);
            }
        }
        
        fs.writeFileSync('c:\\Users\\user\\.gemini\\antigravity\\scratch\\ranjeet-cyber-cafe\\extracted_data.json', JSON.stringify(extracted, null, 2));
        console.log('SUCCESS');
    });
}).on('error', err => console.log('ERROR:', err));
