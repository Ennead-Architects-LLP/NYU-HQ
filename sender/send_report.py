#!/usr/bin/env python
"""
HTML Report Sender
Sends the latest HTML report from local folder to GitHub repository via GitHub Actions.
"""

import os
import sys
import base64
import json
from pathlib import Path
import urllib.request
import urllib.error
from datetime import datetime


def get_script_dir():
    """Gets the directory where this script/exe is located."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).parent


def read_config():
    """Reads configuration from config.json file."""
    script_dir = get_script_dir()
    config_file = script_dir / "config.json"
    
    if not config_file.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_file}\n"
            f"Please create config.json with your GitHub token and repository info."
        )
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        required_fields = ['github_token', 'repo_owner', 'repo_name']
        missing = [field for field in required_fields if field not in config]
        if missing:
            raise ValueError(f"Missing required fields in config.json: {', '.join(missing)}")
        
        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config.json: {e}")


def get_reports_folder():
    """Constructs the reports folder path using the current Windows username."""
    username = os.getenv('USERNAME')
    if not username:
        raise EnvironmentError("Could not detect Windows USERNAME environment variable")
    
    reports_path = (
        f"C:\\Users\\{username}\\Documents\\EnneadTab Ecosystem\\EA_Dist\\Apps\\_revit\\"
        f"EnneaDuck.extension\\EnneadTab Tailor.tab\\Proj. 2534.panel\\"
        f"NYU HQ.pulldown\\monitor_area.pushbutton\\reports"
    )
    
    return Path(reports_path)


def find_latest_html(reports_folder):
    """Finds the most recent HTML file in the reports folder."""
    if not reports_folder.exists():
        raise FileNotFoundError(f"Reports folder not found: {reports_folder}")
    
    # Find all HTML files
    html_files = list(reports_folder.glob("*.html"))
    
    if not html_files:
        raise FileNotFoundError(f"No HTML files found in {reports_folder}")
    
    # Sort by modification time, newest first
    latest_file = max(html_files, key=lambda f: f.stat().st_mtime)
    
    return latest_file


def read_html_content(file_path):
    """Reads the HTML file and returns its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        raise IOError(f"Error reading file {file_path}: {e}")


def trigger_github_workflow(html_content, config):
    """Triggers the GitHub Actions workflow with the HTML content."""
    token = config['github_token']
    repo_owner = config['repo_owner']
    repo_name = config['repo_name']
    
    # Encode HTML content as base64 to safely pass through API
    html_base64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
    
    # GitHub API endpoint for workflow dispatch
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/update-docs.yml/dispatches"
    
    # Prepare the request
    data = json.dumps({
        'ref': 'main',
        'inputs': {
            'html_content': html_base64
        }
    }).encode('utf-8')
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        'User-Agent': 'NYU-HQ-Report-Sender'
    }
    
    print(f"Triggering GitHub Actions workflow...")
    print(f"Repository: {repo_owner}/{repo_name}")
    
    try:
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 204:
                print("[SUCCESS] Successfully triggered GitHub Actions workflow!")
                print("The report will be committed to the repository shortly.")
                print(f"Check: https://github.com/{repo_owner}/{repo_name}/actions")
                return True
            else:
                response_body = response.read().decode('utf-8')
                print(f"[FAILED] Unexpected response code: {response.status}")
                print(f"Response: {response_body}")
                return False
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"[FAILED] HTTP Error {e.code}: {e.reason}")
        print(f"Response: {error_body}")
        return False
    except urllib.error.URLError as e:
        print(f"[FAILED] Network error: {e.reason}")
        return False
    except Exception as e:
        print(f"[FAILED] Unexpected error: {e}")
        return False


def main():
    """Main execution function."""
    print("=" * 60)
    print("HTML Report Sender")
    print("=" * 60)
    
    try:
        # Step 1: Read configuration
        print("\n1. Reading configuration...")
        config = read_config()
        print(f"   Repository: {config['repo_owner']}/{config['repo_name']}")
        
        # Step 2: Get reports folder path
        print("\n2. Locating reports folder...")
        reports_folder = get_reports_folder()
        print(f"   Reports folder: {reports_folder}")
        
        # Step 3: Find latest HTML file
        print("\n3. Finding latest HTML file...")
        latest_html = find_latest_html(reports_folder)
        mod_time = datetime.fromtimestamp(latest_html.stat().st_mtime)
        print(f"   Latest file: {latest_html.name}")
        print(f"   Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 4: Read HTML content
        print("\n4. Reading HTML content...")
        html_content = read_html_content(latest_html)
        print(f"   File size: {len(html_content):,} bytes")
        
        # Step 5: Trigger GitHub workflow
        print("\n5. Triggering GitHub Actions workflow...")
        success = trigger_github_workflow(html_content, config)
        
        if success:
            print("\n" + "=" * 60)
            print("SUCCESS! The HTML report will be committed to the repository.")
            print("=" * 60)
            return 0
        else:
            print("\n" + "=" * 60)
            print("FAILED! Please check the error messages above.")
            print("=" * 60)
            return 1
            
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\n" + "=" * 60)
        print("FAILED!")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit_code = main()
    
    # If running as compiled exe, pause before closing
    if getattr(sys, 'frozen', False):
        try:
            input("\nPress Enter to exit...")
        except (EOFError, KeyboardInterrupt):
            pass
    
    sys.exit(exit_code)
