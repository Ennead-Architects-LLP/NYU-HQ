#!/usr/bin/env python
"""
HTML Report Sender
Sends the latest HTML report from local folder to GitHub repository via GitHub Actions.
"""

import os
import sys
import base64
import glob
from pathlib import Path
import requests
from datetime import datetime


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


def trigger_github_workflow(html_content, repo_owner, repo_name):
    """Triggers the GitHub Actions workflow with the HTML content."""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise EnvironmentError(
            "GITHUB_TOKEN environment variable not set.\n"
            "Please set it with your GitHub Personal Access Token."
        )
    
    # Encode HTML content as base64 to safely pass through API
    html_base64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
    
    # GitHub API endpoint for workflow dispatch
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/update-docs.yml/dispatches"
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'ref': 'main',  # Branch to run the workflow on
        'inputs': {
            'html_content': html_base64
        }
    }
    
    print(f"Triggering GitHub Actions workflow...")
    print(f"Repository: {repo_owner}/{repo_name}")
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 204:
        print("✓ Successfully triggered GitHub Actions workflow!")
        print("Check your repository's Actions tab to see the progress.")
        return True
    else:
        print(f"✗ Failed to trigger workflow. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False


def main():
    """Main execution function."""
    print("=" * 60)
    print("HTML Report Sender")
    print("=" * 60)
    
    try:
        # Configuration - update these if needed
        REPO_OWNER = "szhang"  # Your GitHub username
        REPO_NAME = "NYU-HQ"   # Your repository name
        
        # Step 1: Get reports folder path
        print("\n1. Locating reports folder...")
        reports_folder = get_reports_folder()
        print(f"   Reports folder: {reports_folder}")
        
        # Step 2: Find latest HTML file
        print("\n2. Finding latest HTML file...")
        latest_html = find_latest_html(reports_folder)
        mod_time = datetime.fromtimestamp(latest_html.stat().st_mtime)
        print(f"   Latest file: {latest_html.name}")
        print(f"   Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 3: Read HTML content
        print("\n3. Reading HTML content...")
        html_content = read_html_content(latest_html)
        print(f"   File size: {len(html_content):,} bytes")
        
        # Step 4: Trigger GitHub workflow
        print("\n4. Triggering GitHub Actions workflow...")
        success = trigger_github_workflow(html_content, REPO_OWNER, REPO_NAME)
        
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
        print(f"\n✗ Error: {e}")
        print("\n" + "=" * 60)
        print("FAILED!")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())

