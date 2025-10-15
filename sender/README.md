# HTML Report Sender

This folder contains a Python script that automatically sends the latest HTML report from your local machine to the NYU-HQ GitHub repository.

## How It Works

1. The script finds the latest HTML file in your local reports folder
2. It triggers a GitHub Actions workflow via the GitHub API
3. The workflow commits the HTML file as `docs/index.html` in the repository
4. The updated HTML is automatically published via GitHub Pages

## Setup Instructions

### Step 1: Create GitHub Personal Access Token

1. Go to [GitHub.com](https://github.com) and log in
2. Click your profile picture (top right) → **Settings**
3. Scroll down to **Developer settings** (bottom of left sidebar)
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Give it a note/name: e.g., `NYU-HQ HTML Sender`
7. Set expiration (recommend: **No expiration** or **1 year**)
8. Check the **`repo`** scope (this gives full control of private repositories)
9. Scroll down and click **Generate token**
10. **IMPORTANT**: Copy the token immediately (you won't see it again!)

### Step 2: Set Local Environment Variable

**Option A: Permanent (Recommended)**

Open PowerShell as Administrator and run:

```powershell
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'your_token_here', 'User')
```

Then restart your terminal/PowerShell window.

**Option B: Temporary (Current Session Only)**

In Command Prompt:
```cmd
set GITHUB_TOKEN=your_token_here
```

In PowerShell:
```powershell
$env:GITHUB_TOKEN = "your_token_here"
```

### Step 3: Install Python Dependencies

Open a terminal in the `sender` folder and run:

```bash
pip install -r requirements.txt
```

### Step 4: Configure Repository Information

Open `send_report.py` and update these variables if needed:

```python
REPO_OWNER = "szhang"  # Your GitHub username
REPO_NAME = "NYU-HQ"   # Your repository name
```

## Usage

Run the script from the repository root:

```bash
python sender/send_report.py
```

Or from within the sender folder:

```bash
cd sender
python send_report.py
```

The script will:
- Auto-detect your Windows username
- Find the latest HTML file in your reports folder
- Send it to GitHub via the API
- Trigger the workflow to commit it to the repository

## Troubleshooting

### Error: "GITHUB_TOKEN environment variable not set"

Make sure you've set the `GITHUB_TOKEN` environment variable (see Step 2 above). If you just set it, restart your terminal window.

### Error: "Reports folder not found"

The script expects the reports folder at:
```
C:\Users\{YOUR_USERNAME}\Documents\EnneadTab Ecosystem\EA_Dist\Apps\_revit\EnneaDuck.extension\EnneadTab Tailor.tab\Proj. 2534.panel\NYU HQ.pulldown\monitor_area.pushbutton\reports
```

Make sure this folder exists and contains HTML files.

### Error: "No HTML files found"

Make sure there are `.html` files in the reports folder.

### GitHub API Error

- Check that your Personal Access Token is valid and has `repo` permissions
- Verify the repository owner and name in the script match your GitHub repository
- Make sure the workflow file `.github/workflows/update-docs.yml` exists in your repository

## Monitoring

After running the script successfully, you can monitor the progress:

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Look for the "Update Documentation with HTML Report" workflow
4. Click on the latest run to see the details

## Notes

- The script finds the **most recently modified** HTML file in the reports folder
- If the HTML content is identical to the existing `docs/index.html`, no commit will be made
- The workflow automatically pulls the latest changes before committing to avoid conflicts
- Each commit includes a timestamp in UTC

