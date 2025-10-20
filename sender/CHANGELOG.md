# Changelog

## Version 2.0 - Multi-File Support (2025-10-20)

### Major Changes

**Breaking Change**: The sender now uploads ALL supported files in the reports folder, not just the latest HTML file.

### New Features

- ✅ **Multi-file support**: Now handles HTML, CSS, JS, and JSON files
- ✅ **Smart HTML handling**: Latest HTML file (by modification time) becomes `index.html`
- ✅ **Preserves supporting filenames**: CSS, JS, JSON files keep their original names
- ✅ **Batch upload**: All files in the reports folder are uploaded in a single run
- ✅ **Better progress reporting**: Shows upload status for each file with progress indicators
- ✅ **Partial success handling**: If some files fail, successful uploads are still committed

### What Changed

**Before (v1.x):**
- Found the latest `.html` file
- Uploaded it as `docs/index.html`
- Single file only

**After (v2.0):**
- Finds the **latest** `.html` file → uploads as `index.html`
- Finds ALL `.css`, `.js`, and `.json` files → uploads with original names
- Multiple files in one run
- Example: `report_2025_10_20.html` → `index.html`, plus `styles.css`, `script.js`, `data.json`

### Usage

The usage remains the same - just run the executable:
```bash
NYU_HQ.exe
```

The script will automatically find and upload all supported files.

### Migration Guide

**For Report Generators:**
- You can now split your monolithic HTML into separate files
- Place all files (HTML, CSS, JS, JSON) in the reports folder
- The sender will upload them all automatically

**For Administrators:**
- Rebuild the executable using `build.bat`
- No configuration changes needed
- The new version is backward compatible (still works with single HTML files)

### Technical Details

**Modified Functions:**
- `find_latest_html()` → `find_report_files()` - now finds multiple file types
- `read_html_content()` → `read_file_content()` - handles both text and binary
- `update_github_file()` - now accepts file path, preserves original filename
- `update_all_files()` - new function to batch upload multiple files
- `main()` - updated to handle multiple files

**New Capabilities:**
- Detects file type automatically
- Handles both text (UTF-8) and binary files
- Shows detailed progress for each file
- Reports partial success if some files fail
- Better error messages

### Example Output

```
============================================================
Multi-File Report Sender
Supports: HTML, CSS, JS, JSON
============================================================

1. Reading configuration...
   Repository: Ennead-Architects-LLP/NYU-HQ

2. Locating reports folder...
   Reports folder: C:\Users\...\reports

3. Finding report files (HTML, CSS, JS, JSON)...
   Latest HTML (→ index.html):
      • report_2025_10_20.html (12,345 bytes, modified: 2025-10-20 14:30:25)
   Supporting files (3):
      • styles.css (4,567 bytes, modified: 2025-10-20 14:30:20)
      • script.js (8,901 bytes, modified: 2025-10-20 14:30:22)
      • data.json (123,456 bytes, modified: 2025-10-20 14:30:24)

4. Updating GitHub repository...

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

SUCCESS! All report files have been updated in the repository.
```

### Benefits

1. **Smaller files**: Split large HTML into manageable pieces
2. **Better caching**: Browser can cache CSS/JS separately
3. **Easier maintenance**: Edit CSS without touching HTML
4. **Faster loads**: Separate files load in parallel
5. **Security**: Smaller files less likely to trigger browser warnings
6. **Flexibility**: Other repos can generate any combination of files

### Backward Compatibility

✅ **Fully backward compatible** - If you only have an `index.html`, it will upload just that file. The sender adapts to whatever files are present.

