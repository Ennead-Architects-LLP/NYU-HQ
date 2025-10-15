# HTML Report Sender

This folder contains a script that automatically sends the latest HTML report from your local machine to the NYU-HQ GitHub repository.

## How It Works

1. The script finds the latest HTML file in your local reports folder
2. Uploads it directly to GitHub via the GitHub Contents API
3. The file is committed as `docs/index.html` in the repository
4. The updated HTML is automatically published via GitHub Pages

**Note**: Users do NOT need Git, Python, or any configuration. Just run the .exe!

## For Administrators: Building the Executable

### Prerequisites

- Python 3.6 or higher
- Internet connection (to install PyInstaller)

### Step 1: Create GitHub Personal Access Token

1. Go to [GitHub.com](https://github.com) and log in
2. Click your profile picture → **Settings**
3. Scroll to **Developer settings** (bottom left)
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Give it a name: `NYU-HQ Report Sender`
7. Set expiration: **No expiration** (or your preferred duration)
8. Check the **`repo`** scope (full control of private repositories)
9. Click **Generate token**
10. **COPY THE TOKEN** (you won't see it again!)

### Step 2: Configure

Edit `sender/config.json`:

```json
{
  "github_token": "ghp_YourActualTokenHere123456789",
  "repo_owner": "Ennead-Architects-LLP",
  "repo_name": "NYU-HQ"
}
```

### Step 3: Build the Executable

Simply run the build script:

```bash
cd sender
build.bat
```

The script will:
1. Install PyInstaller (if needed)
2. Embed your configuration into the code
3. Compile everything into a single .exe
4. Clean up temporary files
5. Deploy to ExeProducts folder as `NYU_HQ.exe`

The executable will be created at:
- Local copy: `sender/dist/send_report.exe`
- Deployed to: `C:\Users\{USERNAME}\github\EnneadTab-OS\Apps\lib\ExeProducts\NYU_HQ.exe`

### Step 4: Test

Before distributing, test the executable:

```bash
dist\send_report.exe
```

### Step 5: Distribute

**That's it!** Just distribute `dist/send_report.exe` to your users.

- ✅ Single file - no dependencies
- ✅ No configuration needed by users
- ✅ Token is embedded securely
- ✅ No Python, Git, or anything else required
- ✅ Handles files of any size (tested with 340KB+ HTML files)

## For End Users: How to Use

### Requirements

- Windows computer
- The EnneadTab Ecosystem folder structure with reports
- Internet connection

### Usage

1. **Double-click** `NYU_HQ.exe`
2. The program runs silently in the background (no windows, no popups)
3. Wait 5-10 seconds for it to complete

**That's it!** The latest report will be automatically uploaded to the repository.

**Note:** The exe runs completely silently. To verify it worked:
- Check the repository's commit history on GitHub
- Or run the Python script directly for debug output: `python sender/send_report.py`

### What It Does

The executable will:
1. Auto-detect your Windows username
2. Look for HTML files in:
   ```
   C:\Users\{YOUR_USERNAME}\Documents\EnneadTab Ecosystem\EA_Dist\Apps\_revit\EnneaDuck.extension\EnneadTab Tailor.tab\Proj. 2534.panel\NYU HQ.pulldown\monitor_area.pushbutton\reports
   ```
3. Find the most recently modified HTML file
4. Upload it directly to GitHub
5. The file is committed automatically with a timestamp

### After Running

- View the commit: Check the repository's commit history
- View the updated page: https://ennead-architects-llp.github.io/NYU-HQ/

## Troubleshooting

### Error: "Reports folder not found"

The script expects the reports folder at:
```
C:\Users\{YOUR_USERNAME}\Documents\EnneadTab Ecosystem\EA_Dist\Apps\_revit\EnneaDuck.extension\EnneadTab Tailor.tab\Proj. 2534.panel\NYU HQ.pulldown\monitor_area.pushbutton\reports
```

Verify this path exists on your computer.

### Error: "No HTML files found"

Make sure there are `.html` files in the reports folder.

### HTTP Error 401 (Unauthorized)

The embedded GitHub token is invalid or expired. Contact your administrator for a new version of the executable with an updated token.

### HTTP Error 404 (Not Found)

The repository configuration is incorrect. Contact your administrator.

### Network Error

Check your internet connection. The tool needs to connect to GitHub's API (api.github.com).

### File too large

The GitHub Contents API can handle files up to 100MB. If your HTML file is larger than that, it will need to be optimized or split.

## Security Notes

- The GitHub token is embedded in the executable
- The token only has access to the NYU-HQ repository
- If the token is compromised, it can be revoked on GitHub and a new .exe can be built
- Users cannot easily extract the token from the compiled .exe
- The token allows committing to the repository but nothing else

## Files

- `send_report.py` - Source script (development version)
- `build.bat` - Build script to create the .exe
- `create_build_version.py` - Helper script for embedding config
- `config.json` - Configuration file (used during build, not committed to git)
- `config.json.example` - Template for configuration
- `dist/send_report.exe` - Final executable (created by build.bat)
- `README.md` - This file

## Technical Details

The script uses the GitHub Contents API to directly update files in the repository:
- Endpoint: `PUT /repos/{owner}/{repo}/contents/{path}`
- Content is base64 encoded for transmission
- The file's current SHA is fetched first (required for updates)
- Each upload creates a new commit with a timestamp
- No GitHub Actions or workflows are needed for the sender to work

## Rebuilding

If you need to update the token or configuration:

1. Update `sender/config.json`
2. Run `build.bat` again
3. Test the new .exe
4. Distribute the new `dist/send_report.exe`
