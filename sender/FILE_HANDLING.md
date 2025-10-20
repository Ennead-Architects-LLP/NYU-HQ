# File Handling Summary

## Quick Reference

### What Gets Uploaded

| Local File | GitHub Destination | Notes |
|------------|-------------------|-------|
| `report_2025_10_20.html` (latest) | `docs/index.html` | Renamed to index.html |
| `styles.css` | `docs/styles.css` | Original name preserved |
| `script.js` | `docs/script.js` | Original name preserved |
| `data.json` | `docs/data.json` | Original name preserved |

## Rules

### HTML Files
- **Selection**: The most recently modified HTML file is chosen
- **Naming**: Renamed to `index.html` on upload
- **Example**: `report_2025_10_20_143025.html` → `index.html`

### Supporting Files (CSS, JS, JSON)
- **Selection**: ALL files of these types are uploaded
- **Naming**: Original names are preserved
- **Example**: `styles.css` → `styles.css`

## Example Scenarios

### Scenario 1: Single HTML File
```
Reports folder:
  ├── report.html

GitHub docs/:
  └── index.html  (from report.html)
```

### Scenario 2: HTML + Supporting Files
```
Reports folder:
  ├── report_20251020.html
  ├── styles.css
  ├── script.js
  └── data.json

GitHub docs/:
  ├── index.html     (from report_20251020.html)
  ├── styles.css
  ├── script.js
  └── data.json
```

### Scenario 3: Multiple HTML Files
```
Reports folder:
  ├── old_report.html        (modified: 2025-10-19)
  ├── new_report.html        (modified: 2025-10-20) ← LATEST
  ├── styles.css

GitHub docs/:
  ├── index.html     (from new_report.html - most recent)
  └── styles.css
```

## Important Notes for Report Generators

### 1. HTML Filename Doesn't Matter
Your HTML file can have ANY name:
- ✅ `report.html`
- ✅ `dashboard_2025_10_20.html`
- ✅ `nyu_hq_area_report.html`

It will always become `index.html` on GitHub.

### 2. Supporting Files MUST Match References
If your HTML references supporting files, use the EXACT names:

**✅ CORRECT:**
```html
<!-- In HTML: -->
<link rel="stylesheet" href="styles.css">
<script src="script.js"></script>

<!-- Files in reports folder: -->
styles.css
script.js
```

**❌ WRONG:**
```html
<!-- In HTML: -->
<link rel="stylesheet" href="mystyles.css">

<!-- Files in reports folder: -->
styles.css  ← Mismatch! Browser can't find "mystyles.css"
```

### 3. Multiple HTMLs = Only Latest Uploaded
If you have multiple HTML files, only the newest (by modification time) is uploaded. Old HTML files are ignored.

### 4. All Supporting Files Are Uploaded
ALL CSS, JS, and JSON files are uploaded. No selection by date. If you have old files you don't want, delete them from the reports folder.

## Best Practices

### For Report Generators

1. **Clean the folder first**:
   ```python
   # Delete old files before generating new ones
   for old_file in reports_folder.glob("*.html"):
       old_file.unlink()
   for old_file in reports_folder.glob("*.json"):
       old_file.unlink()
   ```

2. **Use consistent names for supporting files**:
   - Good: `styles.css`, `script.js`, `data.json`
   - Avoid: `styles_2025_10_20.css` (creates duplicates)

3. **Reference files correctly in HTML**:
   ```html
   <link rel="stylesheet" href="styles.css">
   <script src="script.js"></script>
   <!-- Load data dynamically -->
   <script>
   fetch('data.json')
       .then(r => r.json())
       .then(data => renderReport(data));
   </script>
   ```

### Testing Locally

To test before uploading:

1. Open your HTML file directly in a browser
2. Check browser console for 404 errors
3. Make sure all CSS/JS/JSON files load correctly
4. Fix any path/filename mismatches

## GitHub Pages URL Structure

After upload, files are accessible at:

| File | URL |
|------|-----|
| `index.html` | `https://ennead-architects-llp.github.io/NYU-HQ/` |
| `styles.css` | `https://ennead-architects-llp.github.io/NYU-HQ/styles.css` |
| `script.js` | `https://ennead-architects-llp.github.io/NYU-HQ/script.js` |
| `data.json` | `https://ennead-architects-llp.github.io/NYU-HQ/data.json` |

All references in `index.html` should use relative paths (no leading `/`):
- ✅ `href="styles.css"`
- ✅ `src="script.js"`
- ❌ `href="/styles.css"` (won't work on GitHub Pages subdirectory)

## Troubleshooting

### "Page loads but no styling"
- Check if `styles.css` exists in reports folder
- Check if HTML references it correctly: `<link rel="stylesheet" href="styles.css">`
- Check browser console for 404 errors

### "JavaScript not working"
- Check if `script.js` exists in reports folder
- Check if HTML references it correctly: `<script src="script.js"></script>`
- Check browser console for errors

### "Data not loading"
- Check if `data.json` exists in reports folder
- Check if JavaScript fetches it correctly: `fetch('data.json')`
- Check browser console for 404 or JSON parse errors

### "Wrong HTML file uploaded"
- Check modification times - the NEWEST HTML is uploaded
- If you have multiple HTMLs, delete the old ones first
- Or make sure the one you want is the most recently modified

