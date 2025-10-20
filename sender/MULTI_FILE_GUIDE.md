# Multi-File Sender Quick Guide

## Overview

The sender now uploads **all** HTML, CSS, JS, JSON, and image files (PNG, JPG) from the reports folder to GitHub Pages.

## How It Works

### Step 1: Report Generation (handled by other repo)
Your other repository generates these files in the reports folder:
```
reports/
├── report_2025_10_20.html  ← Latest HTML (any filename)
├── styles.css              ← Styling
├── script.js               ← JavaScript functionality
├── data.json               ← Data for the page
├── logo.png                ← Image assets
└── chart.jpg               ← Image assets
```

### Step 2: Sender Upload (this repo)
The sender script:
- Finds the **latest HTML file** (by modification time) → uploads as **index.html**
- Finds all **supporting files** (CSS, JS, JSON, images) → uploads with **original names**

```
GitHub: docs/
├── index.html      ← From latest HTML (renamed)
├── styles.css      ← Original name preserved
├── script.js       ← Original name preserved
├── data.json       ← Original name preserved
├── logo.png        ← Original name preserved
└── chart.jpg       ← Original name preserved
```

### Step 3: GitHub Pages Serving
GitHub Pages automatically serves these files at:
- `https://ennead-architects-llp.github.io/NYU-HQ/` (index.html)
- `https://ennead-architects-llp.github.io/NYU-HQ/styles.css`
- `https://ennead-architects-llp.github.io/NYU-HQ/script.js`
- `https://ennead-architects-llp.github.io/NYU-HQ/data.json`

## Example: Split HTML Structure

### index.html (Simple, Clean)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NYU HQ Report</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="app"></div>
    <script src="script.js"></script>
</body>
</html>
```

### styles.css (All Styling)
```css
body { 
    font-family: 'Roboto', sans-serif; 
    background: #0a0e13;
}
/* ... rest of CSS ... */
```

### script.js (All Logic)
```javascript
// Load data from JSON
fetch('data.json')
    .then(response => response.json())
    .then(data => {
        // Render the data
        renderReport(data);
    });
```

### data.json (All Data)
```json
{
    "departments": [...],
    "rooms": [...],
    "metrics": {...}
}
```

## Benefits

### 1. **Smaller Files**
- Old: 1 file × 400 KB = 400 KB
- New: HTML (10 KB) + CSS (20 KB) + JS (30 KB) + JSON (340 KB) = 400 KB total
- But browsers can cache CSS/JS separately!

### 2. **Better Caching**
- CSS/JS change rarely → cached for days
- Data changes often → only re-download JSON
- Faster page loads for repeat visitors

### 3. **Less Suspicious to Browsers**
- Large single files trigger security warnings
- Multiple smaller files look more "normal"
- Professional website structure

### 4. **Easier Development**
- Edit CSS without touching HTML
- Update data without redeploying code
- Cleaner separation of concerns

### 5. **Parallel Loading**
```
Browser Timeline:
0ms:   Start loading index.html
10ms:  HTML loaded, start loading styles.css and script.js in parallel
30ms:  CSS + JS loaded, start loading data.json
50ms:  Data loaded, render page
```

## Supported File Types

| Extension | Type | Example Use |
|-----------|------|-------------|
| `.html` | Webpage | Main page structure |
| `.css` | Stylesheet | Visual styling |
| `.js` | JavaScript | Interactivity, data loading |
| `.json` | Data | Report data, configuration |

## What the Sender Does

1. **Finds** the latest HTML file (by modification time)
2. **Scans** for supporting files (CSS, JS, JSON)
3. **Uploads** latest HTML as `index.html` (renamed)
4. **Uploads** supporting files with original names (preserved)
5. **Reports** success/failure for each file

## Example Run

```
Finding report files (HTML, CSS, JS, JSON)...
   Latest HTML (→ index.html):
      • report_2025_10_20.html (10,234 bytes, modified: 2025-10-20 14:30:25)
   Supporting files (3):
      • styles.css (23,456 bytes, modified: 2025-10-20 14:30:20)
      • script.js (34,567 bytes, modified: 2025-10-20 14:30:22)
      • data.json (345,678 bytes, modified: 2025-10-20 14:30:24)

Uploading 4 file(s) to GitHub...
Repository: Ennead-Architects-LLP/NYU-HQ
Target folder: docs/

   [1/4] report_2025_10_20.html → index.html
      ✓ SUCCESS - Commit: abc1234

   [2/4] styles.css
      ✓ SUCCESS - Commit: def5678

   [3/4] script.js
      ✓ SUCCESS - Commit: ghi9012

   [4/4] data.json
      ✓ SUCCESS - Commit: jkl3456

============================================================
✓ ALL 4 FILE(S) UPLOADED SUCCESSFULLY!
============================================================
```

## For Other Repo Developers

Your job is to generate these files in the reports folder:

```python
# Example: Generate report files
reports_folder = Path("C:/Users/.../reports")

# Generate HTML
with open(reports_folder / "index.html", "w") as f:
    f.write(generate_html())

# Generate CSS
with open(reports_folder / "styles.css", "w") as f:
    f.write(generate_css())

# Generate JS
with open(reports_folder / "script.js", "w") as f:
    f.write(generate_javascript())

# Generate JSON data
with open(reports_folder / "data.json", "w") as f:
    json.dump(report_data, f, indent=2)
```

The sender will automatically find and upload all of them!

## Notes

- **HTML naming**: Any HTML filename works (e.g., `report_2025_10_20.html`, `dashboard.html`) - the latest one becomes `index.html`
- **Multiple HTMLs**: If multiple HTML files exist, only the newest (by modification time) is uploaded
- **Supporting files**: CSS, JS, JSON files keep their original names - make sure `index.html` references them correctly!
- **No limits on files**: Upload 1 supporting file or 100 supporting files
- **Automatic updates**: Old files in `docs/` are updated, new files are created
- **Time limit**: ~30 seconds total timeout (per your requirements)
- **Backward compatible**: Still works with just a single HTML file (no supporting files needed)

## Testing

To test locally:
```bash
cd sender
python send_report.py
```

This will show detailed output of what's being uploaded.

## Rebuilding the EXE

After these changes, rebuild the executable:
```bash
cd sender
build.bat
```

This will create a new `NYU_HQ.exe` with multi-file support.

